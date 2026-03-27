#!/usr/bin/env python3
"""
Configure RIDOS OS system settings in chroot — Smart Dog Edition
ميزة #4: Zero-Telemetry Fortress — تصفير التتبع + جدار ناري صارم
ميزة #7: Panic Key — تسجيل اختصار لوحة المفاتيح في XFCE
"""
import os, subprocess

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f"  ✍  {path}")

def run(cmd):
    return subprocess.run(cmd, shell=True)


# ════════════════════════════════════════════════════════════════
# 1. معلومات النظام الأساسية
# ════════════════════════════════════════════════════════════════
write('chroot/etc/hostname', 'ridos-os\n')

write('chroot/etc/hosts',
    '127.0.0.1 localhost\n'
    '127.0.1.1 ridos-os\n'
    '::1       localhost ip6-localhost ip6-loopback\n')

write('chroot/etc/locale.gen',
    'en_US.UTF-8 UTF-8\n'
    'ar_IQ.UTF-8 UTF-8\n')

write('chroot/etc/default/locale', 'LANG=en_US.UTF-8\n')
run('chroot chroot locale-gen')
run('chroot chroot ln -sf /usr/share/zoneinfo/Asia/Baghdad /etc/localtime')

# ════════════════════════════════════════════════════════════════
# 2. المستخدم
# ════════════════════════════════════════════════════════════════
run('chroot chroot useradd -m -s /bin/bash '
    '-G sudo,audio,video,netdev,plugdev,bluetooth,dialout ridos 2>/dev/null || true')
run('echo "ridos:ridos" | chroot chroot chpasswd')
run('echo "root:ridos"  | chroot chroot chpasswd')

# ════════════════════════════════════════════════════════════════
# 3. LightDM
# ════════════════════════════════════════════════════════════════
os.makedirs('chroot/etc/lightdm/lightdm.conf.d', exist_ok=True)
write('chroot/etc/lightdm/lightdm.conf.d/50-ridos.conf',
    '[Seat:*]\n'
    'user-session=xfce\n'
    'greeter-session=lightdm-gtk-greeter\n')

write('chroot/etc/lightdm/lightdm-gtk-greeter.conf',
    '[greeter]\n'
    'background=#1a0a2e\n'
    'theme-name=Adwaita-dark\n'
    'icon-theme-name=Papirus-Dark\n'
    'font-name=Noto Sans 11\n'
    'indicators=~host;~spacer;~clock;~spacer;~power\n'
    'clock-format=%A, %d %B %Y  %H:%M\n'
    'position=50%,center 50%,center\n')

# ════════════════════════════════════════════════════════════════
# 4. OS identity
# ════════════════════════════════════════════════════════════════
write('chroot/etc/os-release',
    'PRETTY_NAME="RIDOS OS v1.2.0 Smart Dog"\n'
    'NAME="RIDOS OS"\n'
    'VERSION_ID="1.2.0"\n'
    'VERSION="1.2.0 (Smart Dog)"\n'
    'ID=ridos\n'
    'ID_LIKE=debian\n'
    'HOME_URL="https://github.com/alexeaiskinder-mea/ridos-os"\n'
    'SUPPORT_URL="https://github.com/alexeaiskinder-mea/ridos-os/issues"\n'
    'BUG_REPORT_URL="https://github.com/alexeaiskinder-mea/ridos-os/issues"\n')

write('chroot/etc/issue',
    'RIDOS OS v1.2.0 Smart Dog — Offline AI + SIGINT + Panic Key\n'
    'Username: ridos | Password: ridos\n')

# ════════════════════════════════════════════════════════════════
# 5. systemd — إيقاف تشغيل سريع
# ════════════════════════════════════════════════════════════════
os.makedirs('chroot/etc/systemd/system.conf.d', exist_ok=True)
write('chroot/etc/systemd/system.conf.d/timeout.conf',
    '[Manager]\n'
    'DefaultTimeoutStopSec=5s\n'
    'DefaultTimeoutStartSec=10s\n'
    'ShutdownWatchdogSec=10s\n')

# ════════════════════════════════════════════════════════════════
# 6. ميزة #4 — Zero-Telemetry Fortress
# ════════════════════════════════════════════════════════════════
print("\n[*] Applying Zero-Telemetry Fortress...")

# sysctl hardening — تعطيل IPv6 الغير ضروري وتصلب الشبكة
write('chroot/etc/sysctl.d/99-ridos-hardening.conf', '''
# ─── Zero-Telemetry & Network Hardening ───────────────────────

# تعطيل إعادة توجيه الحزم (لسنا راوتر)
net.ipv4.ip_forward = 0
net.ipv6.conf.all.forwarding = 0

# حماية SYN flood
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 2048
net.ipv4.tcp_synack_retries = 2
net.ipv4.tcp_syn_retries = 5

# منع استكشاف المصدر
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0

# منع ICMP redirects (يستخدم لهجمات MITM)
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0

# تعطيل IPv6 (لتقليل سطح الهجوم)
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1

# تسجيل الحزم المشبوهة
net.ipv4.conf.all.log_martians = 1
net.ipv4.conf.default.log_martians = 1

# منع kernel pointer leak في dmesg
kernel.kptr_restrict = 2
kernel.dmesg_restrict = 1

# تعطيل core dumps (تحتوي بيانات حساسة)
fs.suid_dumpable = 0
kernel.core_pattern = |/bin/false
''')

# UFW — Default Deny (منع افتراضي)
write('chroot/etc/ufw/ufw.conf',
    'ENABLED=yes\n'
    'LOGLEVEL=low\n')

# قواعد UFW — SSH محلي فقط، باقي شيء محظور
write('chroot/etc/ufw/user.rules', '''
*filter
:ufw-user-input - [0:0]
:ufw-user-output - [0:0]
:ufw-user-forward - [0:0]

# السماح بـ Ollama على localhost فقط (المنفذ 11434)
-A ufw-user-input -p tcp --dport 11434 -s 127.0.0.1 -j ACCEPT

# السماح بـ RIDOS Dashboard على localhost فقط
-A ufw-user-input -p tcp --dport 5000 -s 127.0.0.1 -j ACCEPT

# رفض كل شيء آخر وارد
-A ufw-user-input -j DROP

COMMIT
''')

# تعطيل rsyslog remote — لا إرسال سجلات خارجياً
write('chroot/etc/rsyslog.d/99-ridos-no-remote.conf',
    '# RIDOS: Disable remote syslog — Zero Telemetry\n'
    '# $ModLoad imudp\n'
    '# $UDPServerRun 514\n'
    '# $ModLoad imtcp\n'
    '# $InputTCPServerRun 514\n')

# تعطيل خدمات التتبع المعروفة
telemetry_mask = [
    'whoopsie',          # Ubuntu crash reporter
    'apport',            # crash handler
    'popularity-contest',
    'avahi-daemon',      # mDNS/zeroconf — يكشف عن الجهاز على الشبكة
]
for svc in telemetry_mask:
    run(f'chroot chroot systemctl mask {svc} 2>/dev/null || true')
    print(f"  🔇 masked: {svc}")

print("  ✅ Zero-Telemetry Fortress active")

# ════════════════════════════════════════════════════════════════
# 7. ميزة #7 — Panic Key (مفتاح الذعر)
# ════════════════════════════════════════════════════════════════
print("\n[*] Installing Panic Key (Emergency Wipe)...")

# سكربت الطوارئ
write('chroot/usr/local/bin/panic-key', '''#!/bin/bash
# ════════════════════════════════════════════════════════════════
# RIDOS OS — Panic Key Emergency Script
# مفتاح الذعر — طوارئ فورية
# يُفعَّل بـ: Ctrl+Alt+Delete (قابل للتغيير)
# ════════════════════════════════════════════════════════════════
# التحذير: هذا السكربت يُوقف الجهاز فوراً ويمسح المفاتيح الحساسة

# خطوة 1 — إشعار بصري فوري (ثانية واحدة فقط)
notify-send \
  --urgency=critical \
  --expire-time=1000 \
  "🚨 PANIC KEY ACTIVATED — مفتاح الذعر فُعِّل" \
  "Wiping keys and shutting down NOW | مسح المفاتيح والإيقاف الآن" \
  2>/dev/null || true

# خطوة 2 — مسح مفاتيح التشفير من الذاكرة (إن وجدت)
for key_file in \
    /etc/ridos/api.key \
    /home/ridos/.ssh/id_* \
    /home/ridos/.gnupg/private-keys-v1.d/* \
    /tmp/*.key /tmp/*.pem /tmp/*.p12; do
  if [ -f "$key_file" ]; then
    # كتابة أصفار فوق الملف قبل الحذف
    shred -u -z -n 1 "$key_file" 2>/dev/null || rm -f "$key_file"
  fi
done

# خطوة 3 — مسح clipboard
xdotool key ctrl+a 2>/dev/null || true
xclip -selection clipboard /dev/null 2>/dev/null || true
xclip -selection primary   /dev/null 2>/dev/null || true

# خطوة 4 — مسح الذاكرة المؤقتة
sync
echo 3 > /proc/sys/vm/drop_caches 2>/dev/null || true

# خطوة 5 — سجل حدث الطوارئ (محلياً فقط)
echo "[$(date '+%Y-%m-%d %H:%M:%S')] PANIC KEY TRIGGERED — emergency shutdown" \
     >> /var/log/ridos-panic.log 2>/dev/null || true

# خطوة 6 — الإيقاف الفوري (0 ثانية تأخير)
# نستخدم poweroff -f لتجاوز systemd في حالات الطوارئ
/sbin/poweroff -f
''')
run('chmod +x chroot/usr/local/bin/panic-key')

# تسجيل اختصار Panic Key في XFCE — Ctrl+Alt+Delete
# نضعه في الإعدادات الافتراضية للمستخدم ridos
os.makedirs('chroot/home/ridos/.config/xfce4/xfconf/xfce-perchannel-xml', exist_ok=True)
write('chroot/home/ridos/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml',
'''<?xml version="1.0" encoding="UTF-8"?>
<channel name="xfce4-keyboard-shortcuts" version="1.0">
  <property name="commands" type="empty">
    <property name="custom" type="empty">

      <!-- Panic Key: Ctrl+Alt+Delete → مفتاح الذعر -->
      <property name="&lt;Primary&gt;&lt;Alt&gt;Delete" type="string"
                value="panic-key"/>

      <!-- فتح Smart Dog Terminal -->
      <property name="&lt;Primary&gt;&lt;Alt&gt;t" type="string"
                value="xfce4-terminal -e sdt"/>

      <!-- فتح قائمة AI -->
      <property name="&lt;Primary&gt;&lt;Alt&gt;a" type="string"
                value="xfce4-terminal -e \'python3 /opt/ridos/bin/ai_features.py\'"/>

    </property>
  </property>
</channel>
''')

# منح ridos صلاحية تشغيل panic-key بدون كلمة مرور
write('chroot/etc/sudoers.d/ridos-panic',
    'ridos ALL=(ALL) NOPASSWD: /usr/local/bin/panic-key\n'
    'ridos ALL=(ALL) NOPASSWD: /sbin/poweroff\n')
run('chmod 440 chroot/etc/sudoers.d/ridos-panic')

print("  ✅ Panic Key installed → Ctrl+Alt+Delete")

# ════════════════════════════════════════════════════════════════
# 8. خلفية سطح المكتب (Wallpaper)
# ════════════════════════════════════════════════════════════════
print("\n[*] Setting custom wallpaper...")

# نسخ الصورة إلى مجلد الخلفيات
os.makedirs('chroot/usr/share/ridos/wallpapers', exist_ok=True)
run('cp assets/image_0.png chroot/usr/share/ridos/wallpapers/ridos-wallpaper.png 2>/dev/null || '
    'cp image_0.png chroot/usr/share/ridos/wallpapers/ridos-wallpaper.png 2>/dev/null || true')

# إعداد XFCE لاستخدام الخلفية الجديدة لجميع الشاشات
os.makedirs('chroot/home/ridos/.config/xfce4/xfconf/xfce-perchannel-xml', exist_ok=True)
write('chroot/home/ridos/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml',
'''<?xml version="1.0" encoding="UTF-8"?>
<channel name="xfce4-desktop" version="1.0">
  <property name="backdrop" type="empty">
    <property name="screen0" type="empty">
      <property name="monitor0" type="empty">
        <property name="workspace0" type="empty">
          <property name="last-image" type="string"
                    value="/usr/share/ridos/wallpapers/ridos-wallpaper.png"/>
          <property name="image-style" type="int" value="5"/>
          <property name="image-show" type="bool" value="true"/>
          <property name="color-style" type="int" value="0"/>
          <property name="rgba1" type="array">
            <value type="double" value="0.102"/>
            <value type="double" value="0.039"/>
            <value type="double" value="0.18"/>
            <value type="double" value="1"/>
          </property>
        </property>
      </property>
      <!-- دعم شاشة ثانية إن وجدت -->
      <property name="monitor1" type="empty">
        <property name="workspace0" type="empty">
          <property name="last-image" type="string"
                    value="/usr/share/ridos/wallpapers/ridos-wallpaper.png"/>
          <property name="image-style" type="int" value="5"/>
          <property name="image-show" type="bool" value="true"/>
        </property>
      </property>
    </property>
  </property>
</channel>
''')

# LightDM greeter — نفس الصورة كخلفية شاشة تسجيل الدخول
write('chroot/etc/lightdm/lightdm-gtk-greeter.conf',
    '[greeter]\n'
    'background=/usr/share/ridos/wallpapers/ridos-wallpaper.png\n'
    'theme-name=Adwaita-dark\n'
    'icon-theme-name=Papirus-Dark\n'
    'font-name=Noto Sans 11\n'
    'indicators=~host;~spacer;~clock;~spacer;~power\n'
    'clock-format=%A, %d %B %Y  %H:%M\n'
    'position=50%,center 50%,center\n')

print("  ✅ Wallpaper configured")

# ════════════════════════════════════════════════════════════════
# 9. إزالة اختصار Firefox من سطح المكتب
# ════════════════════════════════════════════════════════════════
print("\n[*] Removing Firefox desktop shortcut...")

# حذف أي .desktop لـ Firefox من مجلدات التشغيل التلقائي على سطح المكتب
firefox_shortcuts = [
    'chroot/home/ridos/Desktop/firefox-esr.desktop',
    'chroot/home/ridos/Desktop/firefox.desktop',
    'chroot/usr/share/applications/firefox-esr.desktop',
]
for f in firefox_shortcuts:
    run(f'rm -f {f} 2>/dev/null || true')

# إنشاء NoDisplay override لمنع Firefox من الظهور في القوائم
os.makedirs('chroot/home/ridos/.local/share/applications', exist_ok=True)
write('chroot/home/ridos/.local/share/applications/firefox-esr.desktop',
    '[Desktop Entry]\n'
    'NoDisplay=true\n'
    'Hidden=true\n')

print("  ✅ Firefox shortcut removed from desktop")

# ════════════════════════════════════════════════════════════════
# 10. نظام المساعدة المدمج (Built-in Help System)
# ════════════════════════════════════════════════════════════════
print("\n[*] Installing built-in help system...")

os.makedirs('chroot/opt/ridos/help', exist_ok=True)
os.makedirs('chroot/usr/local/bin', exist_ok=True)

# ── سكربت ridos-help الرئيسي ──────────────────────────────────
write('chroot/usr/local/bin/ridos-help', r'''#!/usr/bin/env python3
"""
RIDOS OS — Built-in Help System
اكتب: ridos-help          لعرض كل الأوامر
اكتب: ridos-help sdt      لمعرفة تفاصيل أمر معين
اكتب: ridos-help sigint   لمعرفة تفاصيل قسم معين
"""
import sys, os, subprocess

P="\033[35m"; C="\033[36m"; G="\033[32m"
Y="\033[33m"; W="\033[37m"; R="\033[31m"
B="\033[1m";  X="\033[0m";  D="\033[2m"

HELP = {
    # ── Smart Dog Terminal ───────────────────────────────────────
    "sdt": {
        "title": "Smart Dog Terminal — الطرفية الذكية",
        "category": "AI Tools",
        "location": "/usr/local/bin/sdt → /opt/ridos/bin/smart_dog_terminal.py",
        "shortcut": "Ctrl+Alt+T  then type: sdt",
        "desc": "Translate natural language (Arabic/English) into Linux commands.",
        "usage": [
            ("sdt",                          "Open interactive mode"),
            ('sdt "أريد فحص الشبكة"',         "Single command — translate and run"),
            ('sdt "scan ports on 192.168.1.1"',"Translate English request"),
            ("sdt !nmap -sV localhost",        "! prefix — execute directly, skip AI"),
            ('sdt ?"explain TCP handshake"',   "? prefix — free question to Ollama AI"),
            ("sdt history",                    "Show last 20 translated commands"),
            ("sdt --help",                     "Show SDT help"),
        ],
        "tips": [
            "SDT works offline — 20+ built-in patterns need no AI",
            "If Ollama is loading, SDT still works via local patterns",
            "Press Ctrl+C anytime to cancel without executing",
        ]
    },

    # ── AI Features ─────────────────────────────────────────────
    "ai": {
        "title": "AI Features Suite — أدوات الذكاء الاصطناعي",
        "category": "AI Tools",
        "location": "/opt/ridos/bin/ai_features.py",
        "shortcut": "Ctrl+Alt+A",
        "desc": "5 AI-powered tools: Terminal, System Doctor, Network Analyzer, Hardware Fixer, Security Scanner.",
        "usage": [
            ("python3 /opt/ridos/bin/ai_features.py",   "Open main menu"),
            ("python3 /opt/ridos/bin/ai_features.py 1", "Direct: AI Terminal"),
            ("python3 /opt/ridos/bin/ai_features.py 2", "Direct: System Doctor"),
            ("python3 /opt/ridos/bin/ai_features.py 3", "Direct: Network Analyzer"),
            ("python3 /opt/ridos/bin/ai_features.py 4", "Direct: Hardware Fixer"),
            ("python3 /opt/ridos/bin/ai_features.py 5", "Direct: Security Scanner"),
        ],
        "tips": [
            "Works offline (rule-based) and online (Claude API if key set)",
            "Set API key: echo 'YOUR_KEY' | sudo tee /etc/ridos/api.key",
            "Bilingual: responds in Arabic and English simultaneously",
        ]
    },

    # ── Ollama ───────────────────────────────────────────────────
    "ollama": {
        "title": "Ollama — Offline AI Engine",
        "category": "AI Tools",
        "location": "/usr/local/bin/ollama  |  service: ollama.service",
        "shortcut": "N/A — runs as background service",
        "desc": "Local AI inference server. Runs Llama 3 8B Q4 model completely offline.",
        "usage": [
            ("systemctl status ollama",              "Check if AI service is running"),
            ("ollama list",                          "Show loaded models"),
            ("ollama run llama3:8b-q4_0",            "Chat directly with Llama 3"),
            ("ollama pull codellama:7b",             "Download additional model (needs internet)"),
            ("curl http://127.0.0.1:11434/api/tags", "API — list models via HTTP"),
            ("sudo systemctl restart ollama",        "Restart AI service"),
            ("journalctl -u ollama -f",              "Watch AI service live logs"),
        ],
        "tips": [
            "Model files are at /opt/ridos/ollama-models/.ollama/models/",
            "First query after boot takes 30-90s (model loads into RAM)",
            "Ollama API is accessible only on localhost — not exposed to network",
        ]
    },

    # ── SIGINT / SDR ─────────────────────────────────────────────
    "sigint": {
        "title": "SIGINT Suite — مركز العمليات اللاسلكية",
        "category": "Radio & SIGINT",
        "location": "/usr/bin/rtl_*, /usr/bin/gqrx, /usr/bin/inspectrum",
        "shortcut": "Launch from terminal or application menu",
        "desc": "RTL-SDR tools for spectrum monitoring, signal capture and protocol decoding.",
        "usage": [
            ("rtl_test -t",                              "Test RTL-SDR hardware connection"),
            ("gqrx",                                     "Open spectrum analyzer GUI"),
            ("inspectrum capture.bin",                   "Analyze IQ recording file"),
            ("rtl_fm -f 96.5e6 -M wbfm -s 200k -r 48k - | aplay -r 48000 -f S16_LE",
                                                         "Listen to FM radio 96.5 MHz"),
            ("rtl_sdr -f 433.92e6 -s 2.048e6 capture.bin",
                                                         "Record 433 MHz IQ data to file"),
            ("rtl_fm -f 152.24e6 -s 22050 - | multimon-ng -t raw -a POCSAG512 -",
                                                         "Decode POCSAG pager traffic"),
            ("rtl_fm -f 144.8e6 -s 24k | direwolf -r 24000 -",
                                                         "Decode APRS packet radio"),
        ],
        "tips": [
            "Plug RTL-SDR dongle — works immediately, no sudo needed (udev rules pre-set)",
            "Gqrx: set Device to 'RTL-SDR / RTL2832U' on first launch",
            "Recommended gain: 30-40 dB for general scanning",
            "Sample rate 2.048 MHz = ~2 MHz bandwidth visible in Gqrx",
        ]
    },

    # ── Security / UFW ───────────────────────────────────────────
    "security": {
        "title": "Zero-Telemetry Fortress — حصن الخصوصية",
        "category": "Security",
        "location": "/etc/ufw/  |  /etc/sysctl.d/99-ridos-hardening.conf",
        "shortcut": "N/A — active by default at boot",
        "desc": "UFW Default Deny firewall + kernel hardening. System is silent by default.",
        "usage": [
            ("sudo ufw status verbose",              "Show firewall status and rules"),
            ("sudo ufw allow from 192.168.1.0/24 to any port 22",
                                                     "Allow SSH from local network only"),
            ("sudo ufw allow out 443/tcp",           "Allow HTTPS outbound"),
            ("sudo ufw deny out to any",             "Block all outbound (air-gap mode)"),
            ("sudo ufw reset",                       "Reset to default deny"),
            ("sysctl -a | grep disable_ipv6",        "Verify IPv6 is disabled"),
            ("ss -tulpn",                            "Check all open ports"),
            ("sudo netstat -tunp",                   "Show all connections with PIDs"),
        ],
        "tips": [
            "Default: ALL inbound blocked. Only localhost services (Ollama:11434, Dashboard:5000) allowed",
            "To update packages temporarily: sudo ufw allow out 80/tcp && sudo ufw allow out 443/tcp",
            "Re-lock after updates: sudo ufw delete allow out 80/tcp",
        ]
    },

    # ── Panic Key ────────────────────────────────────────────────
    "panic": {
        "title": "Panic Key — مفتاح الذعر",
        "category": "Security",
        "location": "/usr/local/bin/panic-key",
        "shortcut": "Ctrl+Alt+Delete",
        "desc": "Emergency script: wipes crypto keys, clears clipboard, forces immediate poweroff.",
        "usage": [
            ("sudo panic-key",                       "Trigger manually from terminal"),
            ("cat /var/log/ridos-panic.log",         "View panic event history"),
            ("sudo nano /usr/local/bin/panic-key",   "Edit the panic script"),
        ],
        "tips": [
            "Sequence: notify (1s) → shred key files → clear clipboard → flush cache → poweroff -f",
            "To test without shutdown: comment out the last line (/sbin/poweroff -f)",
            "Change shortcut: edit ~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml",
            "CAUTION: no confirmation dialog — fires immediately on keypress",
        ]
    },

    # ── Network Tools ────────────────────────────────────────────
    "network": {
        "title": "Network Tools — أدوات الشبكة",
        "category": "Network",
        "location": "/usr/bin/nmap, /usr/bin/tshark, /usr/sbin/iftop, /usr/bin/ss",
        "shortcut": "N/A",
        "desc": "Pre-installed network analysis and monitoring tools.",
        "usage": [
            ("nmap -sV 192.168.1.0/24",              "Scan entire subnet"),
            ("nmap -A -T4 <target>",                 "Aggressive scan: OS + version + scripts"),
            ("sudo tshark -i wlan0 -w /tmp/cap.pcap","Capture packets to file"),
            ("sudo iftop -i wlan0",                  "Real-time bandwidth by host"),
            ("ss -tulpn",                            "Active ports and listening services"),
            ("traceroute 8.8.8.8",                   "Trace network path"),
            ("curl -I https://example.com",          "Check HTTP headers"),
        ],
        "tips": [
            "tshark is CLI Wireshark — analyze with: tshark -r cap.pcap",
            "nmap requires sudo for SYN scan (-sS) and OS detection (-O)",
        ]
    },

    # ── System Tools ─────────────────────────────────────────────
    "system": {
        "title": "System Tools — أدوات النظام",
        "category": "System",
        "location": "/usr/bin/htop, /usr/bin/iotop, /usr/bin/smartctl, /usr/bin/lshw",
        "shortcut": "N/A",
        "desc": "System monitoring, hardware diagnostics, and disk tools.",
        "usage": [
            ("htop",                                 "Interactive process monitor"),
            ("sudo iotop",                           "Disk I/O by process"),
            ("sudo smartctl -a /dev/sda",            "SMART health check on drive"),
            ("sudo lshw -short",                     "Full hardware summary"),
            ("sudo dmidecode -t memory",             "RAM module details"),
            ("lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINT", "Block devices overview"),
            ("df -h",                                "Disk space usage"),
            ("free -h",                              "RAM usage summary"),
            ("neofetch",                             "System info banner"),
            ("journalctl -xe",                       "Recent system logs with errors"),
        ],
        "tips": [
            "smartctl needs sudo — works on SATA/NVMe drives",
            "In Live-RAM mode, /tmp and /var/log are in RAM — lost on reboot",
        ]
    },
}

def print_banner():
    print(f"\n{B}{P}{'═'*58}{X}")
    print(f"{B}{P}  RIDOS OS — Built-in Help   نظام المساعدة المدمج{X}")
    print(f"{B}{P}{'═'*58}{X}\n")

def print_categories():
    cats = {}
    for key, val in HELP.items():
        cat = val["category"]
        cats.setdefault(cat, []).append(key)
    for cat, keys in cats.items():
        print(f"  {B}{C}{cat}{X}")
        for k in keys:
            title = HELP[k]["title"].split("—")[0].strip()
            print(f"    {Y}{k:<12}{X}  {D}{title}{X}")
        print()

def print_topic(topic):
    topic = topic.lower().strip()
    # فحص مطابقة جزئية
    matches = [k for k in HELP if k.startswith(topic) or topic in k]
    if not matches:
        print(f"\n  {R}Topic '{topic}' not found.{X}")
        print(f"  Available: {', '.join(HELP.keys())}\n")
        return
    key = matches[0]
    h = HELP[key]
    print(f"\n{B}{P}{'═'*58}{X}")
    print(f"{B}{P}  {h['title']}{X}")
    print(f"{B}{P}{'═'*58}{X}")
    print(f"\n  {B}Category:{X}  {C}{h['category']}{X}")
    print(f"  {B}Location:{X}  {D}{h['location']}{X}")
    print(f"  {B}Shortcut:{X}  {Y}{h['shortcut']}{X}")
    print(f"\n  {B}Description:{X}")
    print(f"  {W}{h['desc']}{X}\n")
    print(f"  {B}{G}Usage Examples:{X}")
    for cmd, desc in h["usage"]:
        print(f"    {G}{cmd}{X}")
        print(f"      {D}→ {desc}{X}")
    print(f"\n  {B}{Y}Tips:{X}")
    for tip in h["tips"]:
        print(f"    {Y}•{X} {tip}")
    print()

def main():
    print_banner()
    if len(sys.argv) < 2:
        print(f"  {W}Usage:{X}  ridos-help [topic]\n")
        print_categories()
        print(f"  {D}Example: ridos-help sdt | ridos-help sigint | ridos-help ollama{X}\n")
    else:
        topic = " ".join(sys.argv[1:])
        print_topic(topic)

if __name__ == "__main__":
    main()
''')
run('chmod +x chroot/usr/local/bin/ridos-help')

# ── إضافة رسالة MOTD تشير إلى ridos-help ─────────────────────
write('chroot/etc/motd', r'''
 ██████╗ ██╗██████╗  ██████╗ ███████╗
 ██╔══██╗██║██╔══██╗██╔═══██╗██╔════╝
 ██████╔╝██║██║  ██║██║   ██║███████╗
 ██╔══██╗██║██║  ██║██║   ██║╚════██║
 ██║  ██║██║██████╔╝╚██████╔╝███████║
 ╚═╝  ╚═╝╚═╝╚═════╝  ╚═════╝ ╚══════╝
 Smart Dog Edition v1.2.0

  Type  ridos-help          → show all commands & tools
  Type  ridos-help sdt      → Smart Dog Terminal help
  Type  ridos-help sigint   → SDR / Radio tools help
  Type  ridos-help ollama   → Offline AI help
  Type  ridos-help security → Firewall & privacy help
  Type  ridos-help panic    → Panic Key help
  Type  sdt                 → Smart Dog Terminal

''')

print("  ✅ Help system installed → ridos-help")

# ════════════════════════════════════════════════════════════════
# 11. تفعيل الخدمات
# ════════════════════════════════════════════════════════════════
services = [
    'lightdm',
    'NetworkManager',
    'bluetooth',
    'cups',
    'acpid',
    'ssh',
    'spice-vdagentd',
    'ridos-dashboard',
    'ollama',          # Offline AI Brain
    'ufw',             # Zero-Telemetry Firewall
]
for svc in services:
    run(f'chroot chroot systemctl enable {svc} 2>/dev/null || true')

print("\n✅ configure-system.py done — Smart Dog Edition")
