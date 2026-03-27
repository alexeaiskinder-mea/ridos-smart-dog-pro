#!/usr/bin/env python3
"""
RIDOS OS — Smart Dog Terminal (SDT)
ميزة #3: الطرفية الذكية
الطرفية التي تفهم اللغة الطبيعية وتترجمها إلى أوامر Linux

الاستخدام:
  sdt                  → وضع تفاعلي
  sdt "أريد فحص المنافذ"  → تنفيذ مباشر
  sdt --help
"""

import os, sys, json, subprocess, re, readline
from datetime import datetime

# ─── ألوان ────────────────────────────────────────────────────
C = {
    'purple': "\033[35m", 'cyan':   "\033[36m",
    'green':  "\033[32m", 'red':    "\033[31m",
    'yellow': "\033[33m", 'white':  "\033[37m",
    'bold':   "\033[1m",  'reset':  "\033[0m",
    'blue':   "\033[34m",
}
def c(color, text): return f"{C.get(color,'')}{text}{C['reset']}"

# ─── Ollama API (محلي دائماً) ─────────────────────────────────
OLLAMA_URL  = "http://127.0.0.1:11434/api/generate"
OLLAMA_CHAT = "http://127.0.0.1:11434/api/chat"
MODEL       = "llama3:8b-q4_0"

# ─── قاعدة معرفة محلية (fallback إذا لم يستجب Ollama) ────────
# أنماط لغة طبيعية → أوامر Linux مباشرة
LOCAL_PATTERNS = [
    # فحص الشبكة
    (r'(فحص|اختبار|تحقق).*(إشارة|راديو|sdr|ترددات)',
     'rtl_test -t',
     'Test RTL-SDR dongle presence'),
    (r'(فتح|تشغيل|ابدأ).*(gqrx|راديو|sdr)',
     'gqrx &',
     'Open GQRX SDR receiver'),
    (r'(فحص|scan).*(wifi|واي|لاسلكي)',
     'sudo iwlist scan 2>/dev/null | grep -E "ESSID|Signal|Freq"',
     'Scan WiFi networks'),
    (r'(فحص|scan|مسح).*(منافذ|ports).*(محلي|localhost|127)',
     'nmap -sV 127.0.0.1',
     'Scan local ports'),
    (r'(فحص|scan|مسح).*(منافذ|ports)',
     'nmap -sV {TARGET}',
     'Scan ports on target'),

    # مراقبة النظام
    (r'(عرض|إظهار|اظهر).*(المعالج|cpu|processor)',
     'htop',
     'Show CPU and process monitor'),
    (r'(عرض|مراقبة).*(الذاكرة|ram|memory)',
     'free -h && cat /proc/meminfo | grep -E "MemTotal|MemFree|MemAvailable"',
     'Show memory usage'),
    (r'(عرض|مساحة).*(القرص|disk|hdd|ssd)',
     'df -h && lsblk',
     'Show disk space and layout'),
    (r'(حرارة|temperature|درجة)',
     'sensors 2>/dev/null || cat /sys/class/thermal/thermal_zone*/temp 2>/dev/null | awk \'{print $1/1000 " °C"}\'',
     'Show CPU temperature'),
    (r'(شبكة|network|اتصالات|connections)',
     'ss -tulpn',
     'Show active network connections'),

    # الملفات
    (r'(بحث|ابحث|find).*(ملف|file)',
     'find / -name "{QUERY}" 2>/dev/null | head -20',
     'Find files by name'),
    (r'(أكبر|biggest|largest).*(ملفات|files)',
     'du -sh /* 2>/dev/null | sort -rh | head -15',
     'Find largest files'),

    # النظام
    (r'(تحديث|update).*(النظام|system|apt)',
     'sudo apt-get update && sudo apt-get upgrade -y',
     'Update system packages'),
    (r'(إيقاف|أوقف|shutdown).*(النظام|system|الجهاز)',
     'sudo shutdown -h now',
     'Shutdown system'),
    (r'(اعادة|restart|reboot).*(تشغيل|النظام)',
     'sudo reboot',
     'Reboot system'),
    (r'(السجلات|logs|أخطاء|errors)',
     'journalctl -xe --no-pager | tail -50',
     'Show system logs'),

    # Ollama / AI
    (r'(AI|ذكاء|ollama).*(حالة|status|يعمل)',
     'systemctl status ollama && curl -s http://127.0.0.1:11434/api/tags | python3 -m json.tool',
     'Check Ollama AI status'),
    (r'(نماذج|models|موديلات).*(ollama|AI|متاحة)',
     'ollama list',
     'List available AI models'),
]

def ollama_available():
    """التحقق من أن Ollama يعمل محلياً"""
    try:
        import urllib.request
        urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=2)
        return True
    except:
        return False

def ask_ollama(prompt: str, system: str = "") -> str:
    """إرسال سؤال إلى Ollama المحلي"""
    import urllib.request, json
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    body = json.dumps({
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 400}
    }).encode()

    try:
        req = urllib.request.Request(
            OLLAMA_CHAT,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            return data.get("message", {}).get("content", "").strip()
    except Exception as e:
        return f"__OLLAMA_ERROR__: {e}"

def local_match(query: str):
    """
    البحث المحلي في الأنماط — يعمل فوراً بدون Ollama
    يعيد (command, description) أو None
    """
    q = query.lower()
    for pattern, cmd, desc in LOCAL_PATTERNS:
        if re.search(pattern, q, re.IGNORECASE):
            # استخراج الهدف من الجملة إن وجد
            ip_match = re.search(
                r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', query)
            if '{TARGET}' in cmd and ip_match:
                cmd = cmd.replace('{TARGET}', ip_match.group(1))
            elif '{TARGET}' in cmd:
                target = input(c('purple', '  ← أدخل الهدف (IP/hostname): ')).strip()
                cmd = cmd.replace('{TARGET}', target or 'localhost')
            # استخراج اسم ملف إن وجد
            file_match = re.search(r'"([^"]+)"|\'([^\']+)\'|(\S+\.\w+)', query)
            if '{QUERY}' in cmd and file_match:
                fname = file_match.group(1) or file_match.group(2) or file_match.group(3)
                cmd = cmd.replace('{QUERY}', fname)
            elif '{QUERY}' in cmd:
                cmd = cmd.replace('{QUERY}', '*')
            return cmd, desc
    return None

def translate_to_command(query: str) -> tuple[str, str]:
    """
    ترجمة الجملة الطبيعية إلى أمر Linux
    الأولوية: (1) أنماط محلية → (2) Ollama → (3) رسالة خطأ
    """
    # 1) أنماط محلية (فورية)
    local = local_match(query)
    if local:
        return local[0], f"[local] {local[1]}"

    # 2) Ollama (إذا كان يعمل)
    if ollama_available():
        SYSTEM = """أنت مساعد Linux خبير. مهمتك: ترجمة طلبات اللغة الطبيعية (عربي/إنجليزي) إلى أوامر Linux.

قواعد صارمة:
- أجب بأمر واحد فقط على السطر الأول
- على السطر الثاني: شرح قصير (جملة واحدة، عربي أو إنجليزي)
- لا تضف أي شيء آخر
- إذا كان الطلب خطيراً (rm -rf / مثلاً) اكتب: UNSAFE

مثال:
المدخل: أريد فحص المنافذ المفتوحة
المخرج:
nmap -sV 127.0.0.1
فحص المنافذ على الجهاز المحلي"""

        response = ask_ollama(query, SYSTEM)
        if not response.startswith("__OLLAMA_ERROR__"):
            lines = response.strip().splitlines()
            if lines:
                cmd = lines[0].strip().strip('`')
                desc = lines[1].strip() if len(lines) > 1 else "أمر مُقترح من الذكاء الاصطناعي"
                if cmd and cmd != "UNSAFE":
                    return cmd, f"[AI] {desc}"
                elif cmd == "UNSAFE":
                    return "", "⚠ رفض الذكاء الاصطناعي تنفيذ هذا الأمر لأسباب أمنية"

    return "", "❌ لم أتمكن من ترجمة الطلب. جرّب صياغة مختلفة."

def run_command(cmd: str, dry_run: bool = False) -> tuple[int, str]:
    """تنفيذ أمر وإعادة (exit_code, output)"""
    if dry_run:
        return 0, f"[dry-run] {cmd}"
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True,
            text=True, timeout=60
        )
        output = result.stdout
        if result.stderr and result.returncode != 0:
            output += result.stderr
        return result.returncode, output
    except subprocess.TimeoutExpired:
        return -1, "⏱ انتهت المهلة (60 ثانية)"
    except Exception as e:
        return -1, str(e)

def explain_error(cmd: str, error: str) -> str:
    """شرح الخطأ واقتراح الحل — عبر Ollama أو محلياً"""
    # أنماط خطأ شائعة محلياً
    if "command not found" in error:
        pkg = cmd.split()[0]
        return f"💡 الحل: sudo apt-get install {pkg}"
    if "Permission denied" in error or "permission denied" in error:
        return f"💡 الحل: أضف sudo قبل الأمر\n   sudo {cmd}"
    if "No such file" in error:
        return f"💡 الملف غير موجود. تحقق من المسار باستخدام: ls -la"
    if "Network unreachable" in error:
        return f"💡 الشبكة غير متاحة: sudo systemctl restart NetworkManager"

    # Ollama لتحليل الأخطاء الأكثر تعقيداً
    if ollama_available():
        prompt = f"الأمر: {cmd}\nالخطأ: {error[:300]}\nاقترح حلاً قصيراً بالعربية أو الإنجليزية (سطر أو سطرين فقط)"
        resp = ask_ollama(prompt)
        if not resp.startswith("__OLLAMA_ERROR__"):
            return f"💡 {resp}"

    return "💡 راجع `man " + cmd.split()[0] + "` للمزيد"

def print_banner():
    ai_status = c('green', '🟢 Ollama AI جاهز') if ollama_available() \
           else c('yellow', '🟡 Ollama غير متاح — وضع أنماط محلي')
    print(f"""
{c('bold', c('purple', '╔══════════════════════════════════════════════╗'))}
{c('bold', c('purple', '║'))}  {c('bold', c('cyan', 'RIDOS Smart Dog Terminal (SDT)'))}              {c('bold', c('purple', '║'))}
{c('bold', c('purple', '║'))}  {c('white', 'الطرفية الذكية — اكتب بالعربية أو الإنجليزية')}  {c('bold', c('purple', '║'))}
{c('bold', c('purple', '╚══════════════════════════════════════════════╝'))}
  {ai_status}
  {c('yellow', 'اكتب exit أو q للخروج  |  --help للمساعدة')}
""")

def print_help():
    print(f"""
{c('bold', 'أمثلة على الاستخدام:')}

  {c('cyan', 'أريد فحص إشارات الراديو')}
    → rtl_test -t

  {c('cyan', 'افتح برنامج gqrx')}
    → gqrx &

  {c('cyan', 'scan ports on 192.168.1.1')}
    → nmap -sV 192.168.1.1

  {c('cyan', 'أظهر استخدام الذاكرة')}
    → free -h && cat /proc/meminfo | ...

  {c('cyan', 'check ollama status')}
    → systemctl status ollama ...

{c('bold', 'أوامر خاصة:')}
  {c('yellow', '!<أمر>')}    تنفيذ أمر مباشرة (تجاوز الترجمة)
  {c('yellow', '?<سؤال>')}   اسأل الذكاء الاصطناعي سؤالاً حراً
  {c('yellow', 'history')}   عرض سجل الأوامر
  {c('yellow', 'exit')}      خروج
""")

def interactive_mode():
    """الوضع التفاعلي الرئيسي"""
    print_banner()
    history = []

    while True:
        try:
            # Prompt: ridos@sdt:~$
            ai_indicator = c('green', '⚡') if ollama_available() else c('yellow', '◌')
            prompt = f"{c('purple', 'ridos')}{c('white', '@')}{c('cyan', 'sdt')}{ai_indicator}{c('white', ':~$ ')}"
            query = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{c('yellow', 'وداعاً! الكلب الذكي نائم الآن. 🐕')}\n")
            break

        if not query:
            continue
        if query.lower() in ['exit', 'quit', 'q', 'خروج']:
            print(f"\n{c('yellow', 'وداعاً! الكلب الذكي نائم الآن. 🐕')}\n")
            break
        if query.lower() in ['--help', '-h', 'help', 'مساعدة']:
            print_help()
            continue
        if query.lower() == 'history':
            for i, (q, cmd) in enumerate(history[-20:], 1):
                print(f"  {c('cyan', str(i))}. {c('yellow', q)} → {c('green', cmd)}")
            continue

        # تنفيذ مباشر بدون ترجمة (! prefix)
        if query.startswith('!'):
            direct_cmd = query[1:].strip()
            print(c('yellow', f'  ⚡ تنفيذ مباشر: {direct_cmd}'))
            code, out = run_command(direct_cmd)
            if out: print(out)
            if code != 0:
                print(c('red', f'  ✗ exit code {code}'))
            continue

        # سؤال حر للذكاء الاصطناعي (? prefix)
        if query.startswith('?'):
            free_q = query[1:].strip()
            if ollama_available():
                print(c('yellow', '  🤖 يفكر...'))
                resp = ask_ollama(free_q,
                    "أنت خبير Linux. أجب بإيجاز وبالعربية أو الإنجليزية حسب لغة السؤال.")
                print(c('green', f'\n  {resp}\n'))
            else:
                print(c('red', '  ❌ Ollama غير متاح للأسئلة الحرة'))
            continue

        # ─── ترجمة الجملة إلى أمر ─────────────────────────────
        print(c('yellow', '  ↻ أُترجم...'))
        cmd, desc = translate_to_command(query)

        if not cmd:
            print(c('red', f'  ❌ {desc}'))
            continue

        # عرض الأمر المقترح للمراجعة
        print(f"\n  {c('green', '▶')} {c('bold', cmd)}")
        print(f"  {c('cyan', desc)}\n")

        # تأكيد التنفيذ
        try:
            confirm = input(f"  {c('yellow', 'تنفيذ؟ [Y/n]: ')}").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print()
            continue

        if confirm in ['', 'y', 'yes', 'نعم', 'ن']:
            code, output = run_command(cmd)
            if output:
                print(c('white', output))
            if code == 0:
                print(c('green', '  ✓ نجح'))
                history.append((query, cmd))
            else:
                print(c('red', f'  ✗ فشل (exit {code})'))
                hint = explain_error(cmd, output)
                print(c('yellow', f'\n  {hint}\n'))
        else:
            print(c('yellow', '  ↩ ألغيت'))

def single_command_mode(query: str):
    """تنفيذ مباشر من سطر الأوامر: sdt "أريد فحص المنافذ" """
    cmd, desc = translate_to_command(query)
    if not cmd:
        print(c('red', f'❌ {desc}'))
        sys.exit(1)
    print(f"{c('green', '▶')} {c('bold', cmd)}")
    print(c('cyan', desc))
    code, output = run_command(cmd)
    if output: print(output)
    sys.exit(code)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = " ".join(sys.argv[1:])
        if arg in ['--help', '-h']:
            print_help()
        else:
            single_command_mode(arg)
    else:
        interactive_mode()
