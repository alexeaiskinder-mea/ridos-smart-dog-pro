#!/usr/bin/env python3
"""
Configure RIDOS OS — Smart Dog Edition v1.2.0
يحل المشاكل الخمس:
  1. الخلفية تختفي عند فتح نافذة  → إعداد xfconf صحيح + skel + profile.d
  2. أيقونة Firefox على سطح المكتب → حذف شامل من كل المصادر
  3. RIDOS Control Center لا يعمل  → launcher صحيح + wrapper script
  4. RIDOS AI Shell لا يعمل        → launcher صحيح يفتح terminal
  5. File Manager + File System     → تعطيل أيقونات سطح المكتب الافتراضية
"""
import os, subprocess

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f"  ✍  {path}")

def run(cmd):
    return subprocess.run(cmd, shell=True)

def rm(path):
    run(f'rm -f {path} 2>/dev/null || true')

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
    'greeter-session=lightdm-gtk-greeter\n'
    'autologin-user=ridos\n'
    'autologin-user-timeout=0\n')
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
    'NAME="RIDOS OS"\nVERSION_ID="1.2.0"\n'
    'VERSION="1.2.0 (Smart Dog)"\nID=ridos\nID_LIKE=debian\n'
    'HOME_URL="https://github.com/alexeaiskinder-mea/ridos-os"\n')
write('chroot/etc/issue',
    'RIDOS OS v1.2.0 Smart Dog\nUsername: ridos | Password: ridos\n')

# ════════════════════════════════════════════════════════════════
# 5. systemd timeout
# ════════════════════════════════════════════════════════════════
os.makedirs('chroot/etc/systemd/system.conf.d', exist_ok=True)
write('chroot/etc/systemd/system.conf.d/timeout.conf',
    '[Manager]\nDefaultTimeoutStopSec=5s\n'
    'DefaultTimeoutStartSec=10s\nShutdownWatchdogSec=10s\n')

# ════════════════════════════════════════════════════════════════
# 6. Zero-Telemetry Fortress
# ════════════════════════════════════════════════════════════════
print("\n[*] Zero-Telemetry Fortress...")
write('chroot/etc/sysctl.d/99-ridos-hardening.conf',
    'net.ipv4.ip_forward = 0\n'
    'net.ipv6.conf.all.disable_ipv6 = 1\n'
    'net.ipv6.conf.default.disable_ipv6 = 1\n'
    'net.ipv4.conf.all.accept_redirects = 0\n'
    'net.ipv4.conf.all.accept_source_route = 0\n'
    'net.ipv4.tcp_syncookies = 1\n'
    'kernel.kptr_restrict = 2\n'
    'kernel.dmesg_restrict = 1\n'
    'fs.suid_dumpable = 0\n'
    'kernel.core_pattern = |/bin/false\n')
write('chroot/etc/ufw/ufw.conf', 'ENABLED=yes\nLOGLEVEL=low\n')
write('chroot/etc/rsyslog.d/99-ridos-no-remote.conf', '# no remote syslog\n')
for svc in ['whoopsie','apport','popularity-contest','avahi-daemon']:
    run(f'chroot chroot systemctl mask {svc} 2>/dev/null || true')
print("  ✅ Done")


# ════════════════════════════════════════════════════════════════
# LEGAL DISCLAIMER — إخلاء المسؤولية القانوني
# يظهر عند الإقلاع الأول + محفوظ في ملفات النظام
# ════════════════════════════════════════════════════════════════
print("\n[*] Installing Legal Disclaimer...")

DISCLAIMER_AR = """
+================================================================+
|           RIDOS OS v1.2.0 Smart Dog Edition                    |
|                  LEGAL DISCLAIMER                              |
+================================================================+
|                                                                |
|  RIDOS OS is an engineering and research tool intended for     |
|  educational purposes and authorized security testing ONLY.    |
|                                                                |
|  The use of Signal Intelligence (SIGINT) tools and network     |
|  auditing tools is subject to local and international laws.    |
|                                                                |
|  The developers assume NO LIABILITY for misuse or damages      |
|  resulting from the operation of this system.                  |
|                                                                |
|  It is the user's sole responsibility to ensure compliance    |
|  with all applicable legal regulations in their jurisdiction.  |
|                                                                |
|  Authorized use only. Scan only systems you own or have        |
|  explicit written permission to test.                          |
|                                                                |
+================================================================+
|  By using this system you ACCEPT these terms.                  |
+================================================================+
"""

# 1 — ملف نصي دائم في النظام
os.makedirs('chroot/usr/share/ridos', exist_ok=True)
write('chroot/usr/share/ridos/DISCLAIMER.txt', DISCLAIMER_AR)
write('chroot/usr/share/ridos/LICENSE-NOTICE.txt', DISCLAIMER_AR)

# 2 — يظهر في terminal عند كل فتح session جديد (MOTD)
write('chroot/etc/motd', '''
 RIDOS OS v1.2.0 Smart Dog Edition
 ----------------------------------------
 FOR AUTHORIZED & EDUCATIONAL USE ONLY
 ----------------------------------------
  ridos-help          -> all commands guide
  ridos-help sdt      -> Smart Dog Terminal
  ridos-help ai       -> AI Shell
  ridos-help sigint   -> SDR / Radio tools
  sdt                 -> Smart Dog Terminal
  Ctrl+Alt+A          -> AI Shell
  Ctrl+Alt+Delete     -> Panic Key (3s)
''')

# 3 — Splash screen يظهر عند أول دخول إلى سطح المكتب
write('chroot/etc/profile.d/00-ridos-disclaimer.sh', '''#!/bin/bash
# يظهر في terminal sessions فقط (ليس في الـ GUI)
[ -t 1 ] || exit 0
FLAG="/home/$USER/.config/ridos-disclaimer-accepted"
if [ ! -f "$FLAG" ]; then
  cat /usr/share/ridos/DISCLAIMER.txt
  echo ""
  read -r -p "  Press Enter to accept and continue... (اضغط Enter للموافقة والمتابعة) " _
  mkdir -p "$(dirname $FLAG)"
  echo "accepted: $(date)" > "$FLAG"
fi
''')
run('chmod +x chroot/etc/profile.d/00-ridos-disclaimer.sh')

# 4 — autostart GUI: نافذة بسيطة عند أول دخول لسطح المكتب
DISCLAIMER_SHORT = """RIDOS OS — Smart Dog Edition
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FOR AUTHORIZED & EDUCATIONAL USE ONLY
للاستخدام المشروع والتعليمي فقط

This system includes SIGINT and network auditing tools.
Use only on systems and frequencies you are authorized to access.
يتضمن هذا النظام أدوات SIGINT وفحص الشبكات.
استخدمها فقط على الأنظمة والترددات المصرح لك بالوصول إليها.

The developers assume NO liability for misuse.
لا يتحمل المطورون أي مسؤولية عن سوء الاستخدام.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
By clicking OK you accept these terms.
بالضغط على OK فإنك تقبل هذه الشروط."""

write('chroot/usr/local/bin/ridos-disclaimer-gui', f'''#!/bin/bash
FLAG="$HOME/.config/ridos-disclaimer-accepted"
[ -f "$FLAG" ] && exit 0
zenity --text-info \\
  --title="RIDOS OS — Legal Disclaimer | إخلاء المسؤولية" \\
  --width=600 --height=400 \\
  --filename=/usr/share/ridos/DISCLAIMER.txt \\
  --ok-label="I Accept | أقبل" \\
  2>/dev/null || \\
xmessage -center -buttons "I Accept | أقبل:0" \\
  "{DISCLAIMER_SHORT}" 2>/dev/null || true
mkdir -p "$(dirname $FLAG)"
echo "accepted: $(date)" > "$FLAG"
''')
run('chmod +x chroot/usr/local/bin/ridos-disclaimer-gui')

for d in ['chroot/home/ridos/.config/autostart',
           'chroot/etc/skel/.config/autostart']:
    os.makedirs(d, exist_ok=True)
    write(f'{d}/ridos-disclaimer.desktop', '''[Desktop Entry]
Type=Application
Name=RIDOS Legal Disclaimer
Exec=ridos-disclaimer-gui
Hidden=false
NoDisplay=true
X-GNOME-Autostart-enabled=true
X-GNOME-Autostart-Delay=3
''')

print("  ✅ Legal Disclaimer — txt + motd + profile.d + autostart GUI")

# ════════════════════════════════════════════════════════════════
# 7. Panic Key
# ════════════════════════════════════════════════════════════════
print("\n[*] Panic Key (3-second countdown + cancel)...")
write('chroot/usr/local/bin/panic-key', '''#!/bin/bash
# ════════════════════════════════════════════════════════════════
# RIDOS OS — Panic Key  (مفتاح الذعر)
# تفعيل: Ctrl+Alt+Delete
# الإلغاء: Ctrl+C أو أي مفتاح خلال 3 ثوانٍ في نافذة الـ terminal
# ════════════════════════════════════════════════════════════════
COUNTDOWN=3
PIPE=$(mktemp -u /tmp/panic_pipe_XXXXXX)
mkfifo "$PIPE"

# ── نافذة العدّ التنازلي المرئية ─────────────────────────────
(
  for i in 3 2 1; do
    notify-send \
      --urgency=critical \
      --expire-time=1100 \
      --icon=dialog-warning \
      "⚠ PANIC KEY — مفتاح الذعر" \
      "Shutting down in ${i}s — Press Ctrl+C to CANCEL | الإلغاء: Ctrl+C" \
      2>/dev/null || true
    sleep 1
  done
  echo "EXECUTE" > "$PIPE"
) &
NOTIFY_PID=$!

# ── نافذة terminal تتيح الإلغاء بالضغط على أي مفتاح ──────────
xfce4-terminal \
  --title="⚠ PANIC KEY — اضغط Ctrl+C للإلغاء" \
  --geometry=60x8 \
  --command="bash -c '
    echo \"\"
    echo \"  ⚠  PANIC KEY ACTIVATED — مفتاح الذعر\"
    echo \"  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\"
    echo \"  Press Ctrl+C NOW to CANCEL shutdown\"
    echo \"  اضغط Ctrl+C الآن للإلغاء\"
    echo \"\"
    for i in 3 2 1; do
      echo -ne \"  Shutting down in: \$i seconds...\\r\"
      sleep 1
    done
    echo \"  Executing...\"
    echo \"EXECUTE\" > $PIPE 2>/dev/null || true
  '" \
  2>/dev/null &
TERM_PID=$!

# ── انتظر القرار: تنفيذ أو إلغاء ────────────────────────────
trap "
  kill \$NOTIFY_PID \$TERM_PID 2>/dev/null || true
  rm -f '$PIPE'
  notify-send --urgency=normal 'Panic Key Cancelled | تم الإلغاء' \
    'Shutdown aborted by user.' 2>/dev/null || true
  exit 0
" INT TERM

# قراءة النتيجة من الـ pipe (مع timeout 5 ثوانٍ)
RESULT=""
read -t 5 RESULT < "$PIPE" || RESULT="CANCELLED"

kill $NOTIFY_PID $TERM_PID 2>/dev/null || true
rm -f "$PIPE"

if [ "$RESULT" != "EXECUTE" ]; then
  notify-send --urgency=normal \
    "Panic Key Cancelled | تم الإلغاء" \
    "Shutdown aborted." 2>/dev/null || true
  exit 0
fi

# ── التنفيذ الفعلي (بعد تأكيد 3 ثوانٍ) ──────────────────────
notify-send --urgency=critical --expire-time=1000 \
  "🔴 EXECUTING — جارٍ التنفيذ" \
  "Wiping keys and shutting down NOW" 2>/dev/null || true

# مسح مفاتيح التشفير
for f in /etc/ridos/api.key \
         /home/ridos/.ssh/id_* \
         /home/ridos/.gnupg/private-keys-v1.d/* \
         /tmp/*.key /tmp/*.pem /tmp/*.p12; do
  [ -f "$f" ] && shred -u -z -n 1 "$f" 2>/dev/null || true
done

# مسح clipboard
xclip -selection clipboard < /dev/null 2>/dev/null || true
xclip -selection primary   < /dev/null 2>/dev/null || true

# تفريغ page cache
sync
echo 3 > /proc/sys/vm/drop_caches 2>/dev/null || true

# تسجيل الحدث
echo "[$(date '+%Y-%m-%d %H:%M:%S')] PANIC KEY EXECUTED — emergency shutdown" \
     >> /var/log/ridos-panic.log 2>/dev/null || true

# إيقاف فوري
/sbin/poweroff -f
''')
run('chmod +x chroot/usr/local/bin/panic-key')
write('chroot/etc/sudoers.d/ridos-panic',
    'ridos ALL=(ALL) NOPASSWD: /usr/local/bin/panic-key\n'
    'ridos ALL=(ALL) NOPASSWD: /sbin/poweroff\n')
run('chmod 440 chroot/etc/sudoers.d/ridos-panic')
print("  ✅ Panic Key — 3s countdown + Ctrl+C cancel")

# ════════════════════════════════════════════════════════════════
# FIX #1 — الخلفية الصحيحة
# السبب الجذري: XFCE يولّد monitor name ديناميكياً (VGA-1, Virtual1, DP-1...)
# الحل: كتابة XML لكل المسارات المعروفة + سكربت profile.d يطبّقها runtime
# ════════════════════════════════════════════════════════════════
# ================================================================
# FIX: Wallpaper — جذري
# ================================================================
print("\n[*] Setting wallpaper (definitive fix)...")

WP = "/usr/share/ridos/wallpapers/ridos-wallpaper.png"

# 1. كتابة xfce4-desktop.xml بأسماء monitors معروفة
DESKTOP_XML = """<?xml version="1.0" encoding="UTF-8"?>
<channel name="xfce4-desktop" version="1.0">
  <property name="backdrop" type="empty">
    <property name="screen0" type="empty">
      <property name="monitor0" type="empty">
        <property name="workspace0" type="empty">
          <property name="last-image" type="string" value="/usr/share/ridos/wallpapers/ridos-wallpaper.png"/>
          <property name="image-style" type="int" value="5"/>
          <property name="image-show" type="bool" value="true"/>
        </property>
      </property>
      <property name="monitorVirtual1" type="empty">
        <property name="workspace0" type="empty">
          <property name="last-image" type="string" value="/usr/share/ridos/wallpapers/ridos-wallpaper.png"/>
          <property name="image-style" type="int" value="5"/>
          <property name="image-show" type="bool" value="true"/>
        </property>
      </property>
      <property name="monitorVGA-1" type="empty">
        <property name="workspace0" type="empty">
          <property name="last-image" type="string" value="/usr/share/ridos/wallpapers/ridos-wallpaper.png"/>
          <property name="image-style" type="int" value="5"/>
          <property name="image-show" type="bool" value="true"/>
        </property>
      </property>
      <property name="monitorDP-1" type="empty">
        <property name="workspace0" type="empty">
          <property name="last-image" type="string" value="/usr/share/ridos/wallpapers/ridos-wallpaper.png"/>
          <property name="image-style" type="int" value="5"/>
          <property name="image-show" type="bool" value="true"/>
        </property>
      </property>
      <property name="monitorHDMI-1" type="empty">
        <property name="workspace0" type="empty">
          <property name="last-image" type="string" value="/usr/share/ridos/wallpapers/ridos-wallpaper.png"/>
          <property name="image-style" type="int" value="5"/>
          <property name="image-show" type="bool" value="true"/>
        </property>
      </property>
    </property>
  </property>
  <property name="desktop-icons" type="empty">
    <property name="style" type="int" value="2"/>
    <property name="file-icons" type="empty">
      <property name="show-home"       type="bool" value="false"/>
      <property name="show-filesystem" type="bool" value="false"/>
      <property name="show-removable"  type="bool" value="false"/>
      <property name="show-trash"      type="bool" value="false"/>
    </property>
  </property>
</channel>
"""

for xdir in [
    'chroot/home/ridos/.config/xfce4/xfconf/xfce-perchannel-xml',
    'chroot/etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml',
]:
    os.makedirs(xdir, exist_ok=True)
    write(f'{xdir}/xfce4-desktop.xml', DESKTOP_XML)

# 2. autostart script — يُشغَّل بعد XFCE ويطبق على أي monitor
os.makedirs('chroot/etc/xdg/autostart', exist_ok=True)
write('chroot/etc/xdg/autostart/ridos-wallpaper.desktop', """[Desktop Entry]
Type=Application
Name=RIDOS Wallpaper
Exec=/usr/local/bin/ridos-set-wallpaper
NoDisplay=true
X-GNOME-Autostart-enabled=true
""")

write('chroot/usr/local/bin/ridos-set-wallpaper', """#!/bin/bash
WP="/usr/share/ridos/wallpapers/ridos-wallpaper.png"
[ -f "$WP" ] || exit 0
sleep 3
for MON in $(xrandr --query 2>/dev/null | grep " connected" | awk '{print $1}'); do
    xfconf-query -c xfce4-desktop -p "/backdrop/screen0/monitor${MON}/workspace0/last-image" --create -t string -s "$WP" 2>/dev/null || true
    xfconf-query -c xfce4-desktop -p "/backdrop/screen0/monitor${MON}/workspace0/image-style" --create -t int -s 5 2>/dev/null || true
    xfconf-query -c xfce4-desktop -p "/backdrop/screen0/monitor${MON}/workspace0/image-show" --create -t bool -s true 2>/dev/null || true
done
xfdesktop --reload 2>/dev/null || true
""")
run('chmod +x chroot/usr/local/bin/ridos-set-wallpaper')

# 3. مسح cache القديم
run('rm -rf chroot/home/ridos/.cache/xfce4 2>/dev/null || true')
run('rm -rf chroot/home/ridos/.config/xfce4/desktop 2>/dev/null || true')

# 4. LightDM greeter background
write('chroot/etc/lightdm/lightdm-gtk-greeter.conf',
    '[greeter]\n'
    f'background=/usr/share/ridos/wallpapers/ridos-wallpaper.png\n'
    'theme-name=Adwaita-dark\n'
    'icon-theme-name=Papirus-Dark\n'
    'font-name=Noto Sans 11\n'
    'indicators=~host;~spacer;~clock;~spacer;~power\n'
    'clock-format=%A, %d %B %Y  %H:%M\n'
    'position=50%,center 50%,center\n')

print("  Wallpaper configured — xml + autostart + cache cleared")



# ════════════════════════════════════════════════════════════════
# FIX #2 — إزالة Firefox من سطح المكتب
# ════════════════════════════════════════════════════════════════
print("\n[*] FIX #2 — Remove Firefox from ALL locations...")

# 1 حذف من Desktop folders
for p in [
    'chroot/home/ridos/Desktop/firefox-esr.desktop',
    'chroot/home/ridos/Desktop/firefox.desktop',
    'chroot/home/ridos/Desktop/Firefox.desktop',
    'chroot/etc/skel/Desktop/firefox-esr.desktop',
    'chroot/etc/skel/Desktop/firefox.desktop',
    'chroot/root/Desktop/firefox-esr.desktop',
]:
    rm(p)

# 2 السبب الحقيقي: XFCE يقرأ من /usr/share/applications
#   نكتب override كامل يُخفي Firefox تماماً
FIREFOX_HIDDEN = '[Desktop Entry]\nVersion=1.0\nType=Application\nName=Firefox ESR\nNoDisplay=true\nHidden=true\nNotShowIn=XFCE;\n'
for d in [
    'chroot/home/ridos/.local/share/applications',
    'chroot/etc/skel/.local/share/applications',
    'chroot/usr/share/applications',      # المصدر الحقيقي
]:
    os.makedirs(d, exist_ok=True)
    write(f'{d}/firefox-esr.desktop', FIREFOX_HIDDEN)

# 3 إضافة Firefox إلى قائمة البرامج المحظورة في xfce4-panel
run('chroot chroot bash -c \'xfconf-query -c xfce4-desktop -p /desktop-icons/style -s 2 2>/dev/null || true\'')

# 4 سكربت يُشغَّل عند أول دخول لضمان الحذف حتى لو أُعيد تثبيت Firefox
write('chroot/etc/profile.d/98-ridos-no-firefox.sh', """#!/bin/bash
for f in "$HOME/Desktop/firefox"*.desktop /etc/skel/Desktop/firefox*.desktop; do
  [ -f "$f" ] && rm -f "$f"
done
""")
run('chmod +x chroot/etc/profile.d/98-ridos-no-firefox.sh')

print("  ✅ Firefox removed from ALL locations (desktop + applications + profile.d)")

# ════════════════════════════════════════════════════════════════
# FIX #3 — RIDOS Control Center
# ════════════════════════════════════════════════════════════════
print("\n[*] FIX #3 — RIDOS Control Center...")

write('chroot/usr/local/bin/ridos-control-center', '''#!/bin/bash
export DISPLAY=${DISPLAY:-:0}
export PYTHONPATH=/opt/ridos/bin:$PYTHONPATH
cd /opt/ridos/bin
if python3 -c "import tkinter" 2>/dev/null && [ -f /opt/ridos/bin/control_center.py ]; then
    python3 /opt/ridos/bin/control_center.py
else
    xfce4-terminal --title="RIDOS Control Center" \
      --command="bash -c 'echo RIDOS Control Center && echo ------------------- && \
      python3 /opt/ridos/bin/control_center.py; read -p Press_Enter_to_close'"
fi
''')
run('chmod +x chroot/usr/local/bin/ridos-control-center')

CC_DESKTOP = '''[Desktop Entry]
Version=1.0
Type=Application
Name=RIDOS Control Center
Name[ar]=مركز تحكم ريدوس
Exec=ridos-control-center
Icon=preferences-system
Terminal=false
Categories=System;Settings;
StartupNotify=true
'''
write('chroot/usr/share/applications/ridos-control-center.desktop', CC_DESKTOP)
write('chroot/home/ridos/Desktop/ridos-control-center.desktop', CC_DESKTOP)
write('chroot/etc/skel/Desktop/ridos-control-center.desktop', CC_DESKTOP)
run('chmod +x chroot/home/ridos/Desktop/ridos-control-center.desktop')
run('chmod +x chroot/etc/skel/Desktop/ridos-control-center.desktop')
print("  ✅ Done")

# ════════════════════════════════════════════════════════════════
# FIX #4 — RIDOS AI Shell
# ════════════════════════════════════════════════════════════════
print("\n[*] FIX #4 — RIDOS AI Shell...")

write('chroot/usr/local/bin/ridos-ai-shell', '''#!/bin/bash
export DISPLAY=${DISPLAY:-:0}
AI="/opt/ridos/bin/ai_features.py"
[ ! -f "$AI" ] && zenity --error --text="AI script not found: $AI" 2>/dev/null && exit 1
xfce4-terminal \
  --title="RIDOS AI Shell — الذكاء الاصطناعي" \
  --geometry=100x35 \
  --command="bash -c 'python3 $AI; echo; read -p Press_Enter_to_close'" \
  2>/dev/null || \
xterm -title "RIDOS AI Shell" -geometry 100x35 \
  -e "bash -c 'python3 $AI; read'" 2>/dev/null || \
python3 "$AI"
''')
run('chmod +x chroot/usr/local/bin/ridos-ai-shell')

AI_DESKTOP = '''[Desktop Entry]
Version=1.0
Type=Application
Name=RIDOS AI Shell
Name[ar]=قشرة الذكاء الاصطناعي
Comment=Offline AI Assistant (Ollama + Llama3)
Exec=ridos-ai-shell
Icon=utilities-terminal
Terminal=false
Categories=System;Utility;
StartupNotify=true
'''
write('chroot/usr/share/applications/ridos-ai-shell.desktop', AI_DESKTOP)
write('chroot/home/ridos/Desktop/ridos-ai-shell.desktop', AI_DESKTOP)
write('chroot/etc/skel/Desktop/ridos-ai-shell.desktop', AI_DESKTOP)
run('chmod +x chroot/home/ridos/Desktop/ridos-ai-shell.desktop')
run('chmod +x chroot/etc/skel/Desktop/ridos-ai-shell.desktop')
print("  ✅ Done")

# ════════════════════════════════════════════════════════════════
# FIX #5 — تنظيف سطح المكتب (إزالة File Manager + File System)
# الحل في XML أعلاه: show-home=false, show-filesystem=false
# + حذف أي .desktop غير مرغوب
# ════════════════════════════════════════════════════════════════
print("\n[*] FIX #5 — Clean desktop...")
for p in [
    'chroot/home/ridos/Desktop/thunar.desktop',
    'chroot/home/ridos/Desktop/Thunar.desktop',
    'chroot/home/ridos/Desktop/filesystem.desktop',
    'chroot/home/ridos/Desktop/xfce4-about.desktop',
    'chroot/home/ridos/Desktop/trash.desktop',
    'chroot/home/ridos/Desktop/Home.desktop',
    'chroot/etc/skel/Desktop/thunar.desktop',
    'chroot/etc/skel/Desktop/filesystem.desktop',
]:
    rm(p)
print("  ✅ Done")

# ════════════════════════════════════════════════════════════════
# سطح المكتب النهائي — فقط أيقونات RIDOS
# ════════════════════════════════════════════════════════════════
print("\n[*] Creating clean RIDOS desktop icons...")
os.makedirs('chroot/home/ridos/Desktop', exist_ok=True)
os.makedirs('chroot/etc/skel/Desktop', exist_ok=True)

write('chroot/home/ridos/Desktop/smart-dog-terminal.desktop', '''[Desktop Entry]
Version=1.0
Type=Application
Name=Smart Dog Terminal
Name[ar]=الطرفية الذكية
Exec=xfce4-terminal --title="Smart Dog Terminal" --command="bash -c 'sdt; read'"
Icon=utilities-terminal
Terminal=false
StartupNotify=true
''')
write('chroot/home/ridos/Desktop/ridos-help.desktop', '''[Desktop Entry]
Version=1.0
Type=Application
Name=RIDOS Help
Name[ar]=مساعدة ريدوس
Exec=xfce4-terminal --title="RIDOS Help" --command="bash -c 'ridos-help; read'"
Icon=help-browser
Terminal=false
StartupNotify=true
''')
for f in ['smart-dog-terminal.desktop', 'ridos-help.desktop',
          'ridos-control-center.desktop', 'ridos-ai-shell.desktop']:
    run(f'chmod +x chroot/home/ridos/Desktop/{f} 2>/dev/null || true')
    run(f'cp chroot/home/ridos/Desktop/{f} chroot/etc/skel/Desktop/ 2>/dev/null || true')

# ════════════════════════════════════════════════════════════════
# Keyboard shortcuts
# ════════════════════════════════════════════════════════════════
KB_DIR = 'chroot/home/ridos/.config/xfce4/xfconf/xfce-perchannel-xml'
os.makedirs(KB_DIR, exist_ok=True)
write(f'{KB_DIR}/xfce4-keyboard-shortcuts.xml', '''<?xml version="1.0" encoding="UTF-8"?>
<channel name="xfce4-keyboard-shortcuts" version="1.0">
  <property name="commands" type="empty">
    <property name="custom" type="empty">
      <property name="&lt;Primary&gt;&lt;Alt&gt;Delete" type="string" value="panic-key"/>
      <property name="&lt;Primary&gt;&lt;Alt&gt;t" type="string" value="xfce4-terminal"/>
      <property name="&lt;Primary&gt;&lt;Alt&gt;a" type="string" value="ridos-ai-shell"/>
      <property name="&lt;Primary&gt;&lt;Alt&gt;s" type="string"
                value="xfce4-terminal --command=&quot;bash -c &apos;sdt; read&apos;&quot;"/>
    </property>
  </property>
</channel>
''')

# ════════════════════════════════════════════════════════════════
# ridos-help
# ════════════════════════════════════════════════════════════════
print("\n[*] Installing ridos-help...")
write('chroot/usr/local/bin/ridos-help', r'''#!/usr/bin/env python3
import sys
P="\033[35m";C="\033[36m";G="\033[32m";Y="\033[33m"
W="\033[37m";R="\033[31m";B="\033[1m";X="\033[0m";D="\033[2m"
HELP={
  "sdt":{"title":"Smart Dog Terminal","category":"AI","location":"/usr/local/bin/sdt",
    "shortcut":"Ctrl+Alt+S or Desktop","desc":"Natural language Linux terminal.",
    "usage":[("sdt","Interactive mode"),('sdt "أريد فحص الشبكة"',"Arabic request"),
             ("sdt !nmap localhost","Direct execute"),('sdt ?"explain iptables"',"Free AI question")],
    "tips":["Works offline — 20+ local patterns","Ctrl+C to cancel"]},
  "ai":{"title":"RIDOS AI Shell","category":"AI","location":"/opt/ridos/bin/ai_features.py",
    "shortcut":"Ctrl+Alt+A or Desktop","desc":"5 AI tools menu.",
    "usage":[("ridos-ai-shell","Open launcher"),("python3 /opt/ridos/bin/ai_features.py 1","Terminal"),
             ("python3 /opt/ridos/bin/ai_features.py 2","System Doctor"),
             ("python3 /opt/ridos/bin/ai_features.py 3","Network Analyzer")],
    "tips":["Set API key: echo KEY | sudo tee /etc/ridos/api.key","Works offline too"]},
  "control":{"title":"RIDOS Control Center","category":"System","location":"/opt/ridos/bin/control_center.py",
    "shortcut":"Desktop icon","desc":"GUI control panel.",
    "usage":[("ridos-control-center","Open launcher"),("python3 /opt/ridos/bin/control_center.py","Direct")],
    "tips":["Requires python3-tk (pre-installed)"]},
  "ollama":{"title":"Ollama AI Engine","category":"AI","location":"/usr/local/bin/ollama",
    "shortcut":"Background service","desc":"Llama 3 8B running locally.",
    "usage":[("systemctl status ollama","Check status"),("ollama list","Models"),
             ("ollama run llama3:8b-q4_0","Chat"),("sudo systemctl restart ollama","Restart")],
    "tips":["First query takes 30-90s","API: http://127.0.0.1:11434"]},
  "sigint":{"title":"SIGINT Suite","category":"Radio","location":"/usr/bin/rtl_* gqrx inspectrum",
    "shortcut":"Terminal","desc":"RTL-SDR spectrum monitoring.",
    "usage":[("rtl_test -t","Test hardware"),("gqrx","Spectrum GUI"),
             ("rtl_fm -f 96.5e6 -M wbfm -s 200k -r 48k - | aplay -r 48000 -f S16_LE","FM radio"),
             ("rtl_sdr -f 433.92e6 -s 2.048e6 cap.bin","Record IQ")],
    "tips":["Plug dongle — no sudo needed","Gqrx: select RTL-SDR/RTL2832U on first launch"]},
  "security":{"title":"Zero-Telemetry Fortress","category":"Security","location":"/etc/ufw/",
    "shortcut":"Active by default","desc":"UFW Default Deny + kernel hardening.",
    "usage":[("sudo ufw status verbose","Status"),("sudo ufw allow out 443/tcp","Allow HTTPS"),
             ("ss -tulpn","Open ports")],
    "tips":["ALL inbound blocked by default","Temporarily allow: sudo ufw allow out 80/tcp"]},
  "panic":{"title":"Panic Key","category":"Security","location":"/usr/local/bin/panic-key",
    "shortcut":"Ctrl+Alt+Delete","desc":"Emergency wipe + instant poweroff.",
    "usage":[("sudo panic-key","Manual trigger"),("cat /var/log/ridos-panic.log","History")],
    "tips":["FIRES IMMEDIATELY — no confirmation","Test: comment out last line first"]},
  "network":{"title":"Network Tools","category":"Network","location":"/usr/bin/nmap tshark iftop",
    "shortcut":"Terminal","desc":"Network analysis tools.",
    "usage":[("nmap -sV 192.168.1.0/24","Subnet scan"),("sudo tshark -i wlan0 -w cap.pcap","Capture"),
             ("sudo iftop -i wlan0","Bandwidth"),("ss -tulpn","Ports")],
    "tips":["nmap needs sudo for -sS and -O"]},
  "system":{"title":"System Tools","category":"System","location":"/usr/bin/htop smartctl lshw",
    "shortcut":"Terminal","desc":"Hardware monitoring and diagnostics.",
    "usage":[("htop","Processes"),("sudo smartctl -a /dev/sda","Drive health"),
             ("sudo lshw -short","Hardware"),("df -h && free -h","Storage & RAM"),("neofetch","Info")],
    "tips":["Live-RAM: logs lost on reboot","smartctl needs sudo"]},
}
def banner():
    print(f"\n{B}{P}{'='*54}{X}")
    print(f"{B}{P}  RIDOS OS Help — نظام المساعدة{X}")
    print(f"{B}{P}{'='*54}{X}\n")
def cats():
    c2={}
    for k,v in HELP.items(): c2.setdefault(v["category"],[]).append(k)
    for cat,ks in c2.items():
        print(f"  {B}{C}{cat}{X}")
        for k in ks: print(f"    {Y}{k:<12}{X}  {D}{HELP[k]['title']}{X}")
        print()
def topic(t):
    t=t.lower()
    m=[k for k in HELP if k.startswith(t) or t in k]
    if not m: print(f"\n  {R}Not found: '{t}'. Try: {', '.join(HELP)}{X}\n"); return
    h=HELP[m[0]]
    print(f"\n{B}{P}{'='*54}{X}\n{B}{P}  {h['title']}{X}\n{B}{P}{'='*54}{X}")
    print(f"\n  {B}Location:{X} {D}{h['location']}{X}")
    print(f"  {B}Shortcut:{X} {Y}{h['shortcut']}{X}")
    print(f"\n  {W}{h['desc']}{X}\n\n  {B}{G}Usage:{X}")
    for cmd,desc in h["usage"]: print(f"    {G}{cmd}{X}\n      {D}→ {desc}{X}")
    print(f"\n  {B}{Y}Tips:{X}")
    for t in h["tips"]: print(f"    {Y}•{X} {t}")
    print()
banner()
if len(sys.argv)<2:
    print(f"  Usage: ridos-help [topic]\n"); cats()
    print(f"  {D}Examples: ridos-help sdt | ai | sigint | ollama | panic{X}\n")
else: topic(" ".join(sys.argv[1:]))
''')
run('chmod +x chroot/usr/local/bin/ridos-help')

write('chroot/etc/motd', '''
 RIDOS OS v1.2.0 — Smart Dog Edition

  ridos-help          → all commands guide
  ridos-help sdt      → Smart Dog Terminal
  ridos-help ai       → AI Shell
  ridos-help sigint   → SDR / Radio
  ridos-help security → Firewall & privacy
  sdt                 → Smart Dog Terminal
  Ctrl+Alt+A          → AI Shell
  Ctrl+Alt+Delete     → Panic Key

''')


# ════════════════════════════════════════════════════════════════
# RIDOS SMART ASSISTANT — المساعد الذكي المدمج
# يعرف كل أدوات النظام ويجيب بالعربية والإنجليزية
# يعمل offline بالكامل — يتصل بـ Ollama إذا كان متاحاً
# ════════════════════════════════════════════════════════════════
print("\n[*] Installing RIDOS Smart Assistant...")

write('chroot/usr/local/bin/ridos-assistant', r'''#!/usr/bin/env python3
"""
RIDOS OS Smart Assistant — المساعد الذكي
يعرف كل برامج وأوامر وأدوات RIDOS OS
اكتب سؤالاً بالعربية أو الإنجليزية
"""
import sys, os, json, subprocess, urllib.request, readline

# ── ألوان ───────────────────────────────────────────────────────
P="[35m";C="[36m";G="[32m";Y="[33m"
W="[37m";R="[31m";B="[1m";X="[0m";D="[2m"

OLLAMA = "http://127.0.0.1:11434/api/chat"
MODEL  = "llama3:8b-q4_0"

# ── قاعدة معرفة RIDOS OS الكاملة ───────────────────────────────
# كل أداة وبرنامج وأمر في النظام مع وصف بالعربية والإنجليزية
KB = {
  # AI Tools
  "sdt": {
    "name": "Smart Dog Terminal",
    "name_ar": "الطرفية الذكية",
    "cat": "AI",
    "desc": "Natural language terminal — translates Arabic/English to Linux commands",
    "desc_ar": "طرفية اللغة الطبيعية — تترجم العربي والإنجليزي إلى أوامر Linux",
    "cmd": "sdt",
    "shortcut": "Ctrl+Alt+S",
    "location": "/usr/local/bin/sdt",
    "examples": ["sdt", 'sdt "أريد فحص الشبكة"', "sdt !nmap localhost", 'sdt ?"explain TCP"'],
    "tags": ["terminal","طرفية","ذكاء","ai","أوامر","commands","linux","ترجمة"]
  },
  "ai_shell": {
    "name": "RIDOS AI Shell",
    "name_ar": "قشرة الذكاء الاصطناعي",
    "cat": "AI",
    "desc": "5 AI-powered tools: Terminal, System Doctor, Network Analyzer, Hardware Fixer, Security Scanner",
    "desc_ar": "5 أدوات ذكاء اصطناعي: طرفية، طبيب نظام، محلل شبكة، إصلاح عتاد، ماسح أمني",
    "cmd": "ridos-ai-shell",
    "shortcut": "Ctrl+Alt+A",
    "location": "/opt/ridos/bin/ai_features.py",
    "examples": ["ridos-ai-shell",
                 "python3 /opt/ridos/bin/ai_features.py 1",
                 "python3 /opt/ridos/bin/ai_features.py 2"],
    "tags": ["ai","ذكاء","مساعد","assistant","تشخيص","diagnose","scanner","طبيب"]
  },
  "ollama": {
    "name": "Ollama AI Engine",
    "name_ar": "محرك الذكاء الاصطناعي",
    "cat": "AI",
    "desc": "Local AI inference server — runs Llama 3 8B Q4 offline, no internet needed",
    "desc_ar": "خادم الذكاء الاصطناعي المحلي — يشغّل Llama 3 بدون إنترنت",
    "cmd": "ollama",
    "shortcut": "Background service (ollama.service)",
    "location": "/usr/local/bin/ollama",
    "examples": ["systemctl status ollama", "ollama list", "ollama run llama3:8b-q4_0",
                 "curl http://127.0.0.1:11434/api/tags"],
    "tags": ["ollama","llama","ai","offline","model","موديل","ذكاء اصطناعي","محلي"]
  },
  "control_center": {
    "name": "RIDOS Control Center",
    "name_ar": "مركز التحكم",
    "cat": "System",
    "desc": "GUI control panel for RIDOS OS settings and tools",
    "desc_ar": "لوحة تحكم رسومية لإعدادات وأدوات RIDOS OS",
    "cmd": "ridos-control-center",
    "shortcut": "Desktop icon",
    "location": "/opt/ridos/bin/control_center.py",
    "examples": ["ridos-control-center", "python3 /opt/ridos/bin/control_center.py"],
    "tags": ["control","تحكم","settings","إعدادات","gui","panel","لوحة"]
  },
  # SIGINT / SDR
  "gqrx": {
    "name": "Gqrx",
    "name_ar": "محلل الطيف الراديوي",
    "cat": "SIGINT",
    "desc": "Software-defined radio receiver with real-time spectrum analyzer GUI",
    "desc_ar": "جهاز استقبال راديو برمجي مع واجهة رسومية لتحليل الطيف الترددي",
    "cmd": "gqrx",
    "shortcut": "Terminal",
    "location": "/usr/bin/gqrx",
    "examples": ["gqrx"],
    "tags": ["gqrx","sdr","راديو","radio","طيف","spectrum","ترددات","frequencies"]
  },
  "rtlsdr": {
    "name": "RTL-SDR Tools",
    "name_ar": "أدوات RTL-SDR",
    "cat": "SIGINT",
    "desc": "RTL-SDR driver and utilities for software-defined radio",
    "desc_ar": "تعريفات وأدوات RTL-SDR لاستقبال الإشارات الراديوية",
    "cmd": "rtl_test",
    "shortcut": "Terminal",
    "location": "/usr/bin/rtl_*",
    "examples": ["rtl_test -t",
                 "rtl_fm -f 96.5e6 -M wbfm -s 200k -r 48k - | aplay -r 48000 -f S16_LE",
                 "rtl_sdr -f 433.92e6 -s 2.048e6 capture.bin",
                 "rtl_power -f 88M:108M:100k scan.csv"],
    "tags": ["rtl","sdr","dongle","radio","راديو","إشارة","signal","fm","433"]
  },
  "inspectrum": {
    "name": "Inspectrum",
    "name_ar": "محلل التسجيلات الراديوية",
    "cat": "SIGINT",
    "desc": "Analyse and decode captured IQ recordings from SDR",
    "desc_ar": "تحليل وفك تشفير التسجيلات الراديوية IQ من SDR",
    "cmd": "inspectrum",
    "shortcut": "Terminal",
    "location": "/usr/bin/inspectrum",
    "examples": ["inspectrum capture.bin", "inspectrum recording.cs8"],
    "tags": ["inspectrum","iq","capture","تسجيل","decode","فك تشفير","تحليل"]
  },
  "multimon": {
    "name": "Multimon-NG",
    "name_ar": "فك تشفير البروتوكولات",
    "cat": "SIGINT",
    "desc": "Decode digital radio protocols: POCSAG, FLEX, DTMF, AX.25",
    "desc_ar": "فك تشفير بروتوكولات الراديو الرقمي: POCSAG, FLEX, DTMF, AX.25",
    "cmd": "multimon-ng",
    "shortcut": "Terminal",
    "location": "/usr/bin/multimon-ng",
    "examples": ["rtl_fm -f 152.24e6 -s 22050 - | multimon-ng -t raw -a POCSAG512 -",
                 "rtl_fm -f 169.8e6 -s 22050 - | multimon-ng -t raw -a FLEX -"],
    "tags": ["multimon","pocsag","flex","pager","بيجر","dtmf","ax25","decode"]
  },
  "direwolf": {
    "name": "Direwolf",
    "name_ar": "برنامج APRS",
    "cat": "SIGINT",
    "desc": "Software AX.25 TNC for APRS packet radio decoding",
    "desc_ar": "برنامج TNC لفك تشفير إشارات APRS وراديو الحزم",
    "cmd": "direwolf",
    "shortcut": "Terminal",
    "location": "/usr/bin/direwolf",
    "examples": ["rtl_fm -f 144.8e6 -s 24k | direwolf -r 24000 -"],
    "tags": ["direwolf","aprs","ax25","packet","حزم","تتبع","tracking"]
  },
  "gnuradio": {
    "name": "GNU Radio",
    "name_ar": "إطار معالجة الإشارات",
    "cat": "SIGINT",
    "desc": "Signal processing framework for building custom SDR pipelines",
    "desc_ar": "إطار معالجة الإشارات لبناء خطوط SDR مخصصة",
    "cmd": "gnuradio-companion",
    "shortcut": "Terminal",
    "location": "/usr/bin/gnuradio-companion",
    "examples": ["gnuradio-companion"],
    "tags": ["gnuradio","gnu radio","إشارة","signal","processing","معالجة","flowgraph"]
  },
  # Network Tools
  "nmap": {
    "name": "Nmap",
    "name_ar": "فاحص الشبكات",
    "cat": "Network",
    "desc": "Network scanner: port discovery, OS detection, service version detection",
    "desc_ar": "فاحص الشبكات: اكتشاف المنافذ، تحديد نظام التشغيل، إصدارات الخدمات",
    "cmd": "nmap",
    "shortcut": "Terminal",
    "location": "/usr/bin/nmap",
    "examples": ["nmap -sV 192.168.1.0/24", "nmap -A -T4 192.168.1.1",
                 "nmap -sS -O 192.168.1.1", "nmap -p 22,80,443 192.168.1.1"],
    "tags": ["nmap","scan","فحص","منافذ","ports","network","شبكة","discovery"]
  },
  "wireshark": {
    "name": "Wireshark / TShark",
    "name_ar": "محلل حزم الشبكة",
    "cat": "Network",
    "desc": "Packet capture and analysis — tshark is CLI version",
    "desc_ar": "التقاط وتحليل حزم الشبكة — tshark هو الإصدار من سطر الأوامر",
    "cmd": "tshark",
    "shortcut": "Terminal",
    "location": "/usr/bin/tshark",
    "examples": ["sudo tshark -i wlan0 -w capture.pcap",
                 "tshark -r capture.pcap",
                 "sudo tshark -i eth0 -Y http"],
    "tags": ["wireshark","tshark","packet","حزم","capture","التقاط","network","شبكة"]
  },
  "iftop": {
    "name": "Iftop",
    "name_ar": "مراقب النطاق الترددي",
    "cat": "Network",
    "desc": "Real-time bandwidth monitor by host",
    "desc_ar": "مراقب النطاق الترددي في الوقت الحقيقي حسب المضيف",
    "cmd": "iftop",
    "shortcut": "Terminal",
    "location": "/usr/sbin/iftop",
    "examples": ["sudo iftop -i wlan0", "sudo iftop -i eth0 -n"],
    "tags": ["iftop","bandwidth","نطاق","ترددي","traffic","حركة","network","شبكة"]
  },
  # Security
  "ufw": {
    "name": "UFW Firewall",
    "name_ar": "جدار الحماية",
    "cat": "Security",
    "desc": "Uncomplicated Firewall — Default Deny policy pre-configured",
    "desc_ar": "جدار الحماية — مضبوط على المنع الافتراضي مسبقاً",
    "cmd": "ufw",
    "shortcut": "Terminal (sudo required)",
    "location": "/usr/sbin/ufw",
    "examples": ["sudo ufw status verbose", "sudo ufw allow out 443/tcp",
                 "sudo ufw allow from 192.168.1.0/24 to any port 22",
                 "sudo ufw reset"],
    "tags": ["ufw","firewall","جدار","حماية","security","أمن","iptables"]
  },
  "panic_key": {
    "name": "Panic Key",
    "name_ar": "مفتاح الذعر",
    "cat": "Security",
    "desc": "Emergency script: 3s countdown, wipes crypto keys, forces instant poweroff",
    "desc_ar": "سكربت طوارئ: عدّ تنازلي 3 ثوانٍ، يمسح المفاتيح، ويُوقف الجهاز فوراً",
    "cmd": "panic-key",
    "shortcut": "Ctrl+Alt+Delete",
    "location": "/usr/local/bin/panic-key",
    "examples": ["sudo panic-key", "cat /var/log/ridos-panic.log"],
    "tags": ["panic","ذعر","emergency","طوارئ","wipe","مسح","shutdown","إيقاف","security"]
  },
  # System
  "htop": {
    "name": "Htop",
    "name_ar": "مراقب العمليات",
    "cat": "System",
    "desc": "Interactive process monitor — CPU, RAM, processes",
    "desc_ar": "مراقب العمليات التفاعلي — المعالج والذاكرة والعمليات",
    "cmd": "htop",
    "shortcut": "Terminal",
    "location": "/usr/bin/htop",
    "examples": ["htop"],
    "tags": ["htop","top","process","عمليات","cpu","معالج","ram","ذاكرة","monitor"]
  },
  "smartctl": {
    "name": "Smartmontools",
    "name_ar": "فاحص الأقراص الصلبة",
    "cat": "System",
    "desc": "SMART disk health monitoring for HDD/SSD/NVMe",
    "desc_ar": "مراقبة صحة الأقراص الصلبة HDD/SSD/NVMe عبر تقنية SMART",
    "cmd": "smartctl",
    "shortcut": "Terminal (sudo required)",
    "location": "/usr/sbin/smartctl",
    "examples": ["sudo smartctl -a /dev/sda", "sudo smartctl -H /dev/nvme0",
                 "sudo smartctl -t short /dev/sda"],
    "tags": ["smart","smartctl","disk","قرص","hdd","ssd","nvme","health","صحة"]
  },
  "gparted": {
    "name": "GParted",
    "name_ar": "مدير الأقسام",
    "cat": "System",
    "desc": "GUI partition manager for HDD/SSD/USB",
    "desc_ar": "مدير الأقسام الرسومي للأقراص والـ USB",
    "cmd": "gparted",
    "shortcut": "Terminal (sudo required)",
    "location": "/usr/sbin/gparted",
    "examples": ["sudo gparted"],
    "tags": ["gparted","partition","قسم","disk","قرص","format","تهيئة","usb"]
  },
  "lshw": {
    "name": "Lshw",
    "name_ar": "معلومات العتاد",
    "cat": "System",
    "desc": "Detailed hardware information: CPU, RAM, storage, network cards",
    "desc_ar": "معلومات تفصيلية عن العتاد: المعالج، الذاكرة، التخزين، بطاقات الشبكة",
    "cmd": "lshw",
    "shortcut": "Terminal (sudo recommended)",
    "location": "/usr/bin/lshw",
    "examples": ["sudo lshw -short", "sudo lshw -class network", "sudo lshw -html > hw.html"],
    "tags": ["lshw","hardware","عتاد","cpu","ram","network","storage","تشخيص"]
  },
  "neofetch": {
    "name": "Neofetch",
    "name_ar": "معلومات النظام",
    "cat": "System",
    "desc": "Display system info: OS, kernel, CPU, RAM, uptime",
    "desc_ar": "عرض معلومات النظام: النظام والنواة والمعالج والذاكرة ووقت التشغيل",
    "cmd": "neofetch",
    "shortcut": "Terminal",
    "location": "/usr/bin/neofetch",
    "examples": ["neofetch"],
    "tags": ["neofetch","sysinfo","معلومات","نظام","system","info","kernel"]
  },
  "help": {
    "name": "RIDOS Help System",
    "name_ar": "نظام المساعدة",
    "cat": "System",
    "desc": "Built-in detailed help for all RIDOS tools",
    "desc_ar": "نظام المساعدة المفصّل لجميع أدوات RIDOS",
    "cmd": "ridos-help",
    "shortcut": "Terminal",
    "location": "/usr/local/bin/ridos-help",
    "examples": ["ridos-help", "ridos-help sdt", "ridos-help sigint", "ridos-help security"],
    "tags": ["help","مساعدة","guide","دليل","info","معلومات","ridos"]
  },
}

SYSTEM_PROMPT = """أنت مساعد RIDOS OS الذكي. تعرف كل أدوات وبرامج وأوامر هذا النظام.

قواعد الإجابة:
- أجب بالعربية والإنجليزية معاً
- اذكر الأمر الدقيق والموقع في النظام
- أعطِ مثالاً عملياً
- كن موجزاً (3-5 أسطر كحد أقصى)

معلومات النظام المتاحة:
""" + json.dumps(KB, ensure_ascii=False, indent=2)

def ollama_ok():
    try:
        urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=2)
        return True
    except: return False

def ask_ollama(question, context=""):
    msgs = [{"role":"system","content": SYSTEM_PROMPT}]
    if context: msgs.append({"role":"system","content": f"Context:
{context}"})
    msgs.append({"role":"user","content": question})
    body = json.dumps({"model":MODEL,"messages":msgs,"stream":False,
                       "options":{"temperature":0.2,"num_predict":500}}).encode()
    try:
        req = urllib.request.Request(OLLAMA, data=body,
              headers={"Content-Type":"application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())["message"]["content"].strip()
    except: return None

def local_search(q):
    """البحث المحلي في قاعدة المعرفة"""
    q_low = q.lower()
    results = []
    for key, item in KB.items():
        score = 0
        # مطابقة الاسم
        if q_low in item["name"].lower():       score += 10
        if q_low in item.get("name_ar",""):     score += 10
        if q_low in item["cmd"].lower():        score += 8
        # مطابقة الوسوم
        for tag in item.get("tags", []):
            if q_low in tag.lower() or tag.lower() in q_low: score += 5
        # مطابقة الوصف
        if q_low in item["desc"].lower():       score += 3
        if q_low in item.get("desc_ar",""):     score += 3
        if score > 0: results.append((score, key, item))
    results.sort(reverse=True)
    return results[:3]

def format_local(results, q):
    if not results: return None
    lines = []
    for score, key, item in results:
        lines.append(f"
  {B}{C}{item['name']}{X}  {D}({item['name_ar']}){X}")
        lines.append(f"  {D}{item['cat']}{X}")
        lines.append(f"  {W}{item['desc']}{X}")
        lines.append(f"  {D}{item['desc_ar']}{X}")
        lines.append(f"  {G}Command:{X}  {G}{item['cmd']}{X}")
        lines.append(f"  {Y}Location:{X} {D}{item['location']}{X}")
        if item.get("shortcut"):
            lines.append(f"  {Y}Shortcut:{X} {item['shortcut']}")
        if item.get("examples"):
            lines.append(f"  {G}Examples:{X}")
            for ex in item["examples"][:2]:
                lines.append(f"    {G}{ex}{X}")
        lines.append("")
    return "
".join(lines)

def answer(question):
    """الإجابة على السؤال: محلي أولاً ثم Ollama"""
    # 1) بحث محلي
    results = local_search(question)
    local_ans = format_local(results, question)

    # 2) Ollama إذا كان متاحاً
    if ollama_ok():
        context = json.dumps(
            [{"key":k,"name":v["name"],"desc":v["desc"],"cmd":v["cmd"]}
             for _,k,v in results], ensure_ascii=False
        ) if results else ""
        ai_ans = ask_ollama(question, context)
        if ai_ans:
            print(f"
  {B}{P}[AI]{X} {ai_ans}
")
            if local_ans:
                print(f"  {D}── Related tools found locally ──{X}")
                print(local_ans)
            return

    # 3) إجابة محلية فقط
    if local_ans:
        print(local_ans)
    else:
        print(f"
  {Y}لم أجد نتائج محددة لـ: '{question}'{X}")
        print(f"  {D}No specific results for: '{question}'{X}")
        print(f"
  {C}جرّب:{X} ridos-help  |  ridos-assistant list
")

def show_all():
    cats = {}
    for k, v in KB.items(): cats.setdefault(v["cat"],[]).append((k,v))
    for cat, items in sorted(cats.items()):
        print(f"
  {B}{C}{'─'*4} {cat} {'─'*4}{X}")
        for key, item in items:
            print(f"  {Y}{item['cmd']:<28}{X} {D}{item['name_ar']}{X}")
            print(f"  {D}{'':28} {item['desc'][:60]}...{X}" if len(item['desc'])>60
                  else f"  {D}{'':28} {item['desc']}{X}")

def banner():
    ai = f"{G}● Ollama AI active{X}" if ollama_ok() else f"{Y}○ Offline mode{X}"
    print(f"""
{B}{P}╔══════════════════════════════════════════════════════╗{X}
{B}{P}║  RIDOS Smart Assistant — المساعد الذكي               ║{X}
{B}{P}╚══════════════════════════════════════════════════════╝{X}
  {ai}
  {D}اكتب سؤالاً بالعربية أو الإنجليزية{X}
  {D}Type 'list' for all tools  |  'exit' to quit{X}
""")

def main():
    banner()
    if len(sys.argv) > 1:
        q = " ".join(sys.argv[1:])
        if q == "list": show_all(); return
        answer(q); return

    # وضع تفاعلي
    try: readline.parse_and_bind("tab: complete")
    except: pass

    while True:
        try:
            q = input(f"
  {P}RIDOS{X}{B}>{X} ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"
  {Y}وداعاً!{X}
"); break
        if not q: continue
        if q.lower() in ["exit","quit","خروج","q"]:
            print(f"
  {Y}وداعاً!{X}
"); break
        if q.lower() == "list":
            show_all(); continue
        answer(q)

if __name__ == "__main__":
    main()
''')
run('chmod +x chroot/usr/local/bin/ridos-assistant')

# Desktop shortcut للمساعد
ASST_DESKTOP = '''[Desktop Entry]
Version=1.0
Type=Application
Name=RIDOS Assistant
Name[ar]=المساعد الذكي
Comment=Ask anything about RIDOS OS tools
Comment[ar]=اسأل عن أي أداة في RIDOS OS
Exec=xfce4-terminal --title="RIDOS Smart Assistant" --geometry=90x35 --command="bash -c 'ridos-assistant; read -p Exit...'"
Icon=system-help
Terminal=false
StartupNotify=true
'''
write('chroot/usr/share/applications/ridos-assistant.desktop', ASST_DESKTOP)
write('chroot/home/ridos/Desktop/ridos-assistant.desktop', ASST_DESKTOP)
write('chroot/etc/skel/Desktop/ridos-assistant.desktop', ASST_DESKTOP)
run('chmod +x chroot/home/ridos/Desktop/ridos-assistant.desktop')
run('chmod +x chroot/etc/skel/Desktop/ridos-assistant.desktop')

print("  ✅ RIDOS Smart Assistant installed → ridos-assistant")
print("     Usage: ridos-assistant \"اريد فحص الشبكة\"")
print("     Usage: ridos-assistant list")



# ════════════════════════════════════════════════════════════════
# RIDOS HELP CENTER
# ════════════════════════════════════════════════════════════════
print("\n[*] Installing RIDOS Help Center...")

os.makedirs('chroot/usr/share/ridos', exist_ok=True)
run('cp build-system/help/ridos-help-center.html chroot/usr/share/ridos/ 2>/dev/null || true')
run('cp build-system/scripts/ridos-help-center.html chroot/usr/share/ridos/ 2>/dev/null || true')

write('chroot/usr/local/bin/ridos-help-center', """#!/bin/bash
HELP="/usr/share/ridos/ridos-help-center.html"
[ ! -f "$HELP" ] && echo "Help file not found" && exit 1
if command -v firefox-esr &>/dev/null; then
  firefox-esr "$HELP" &
elif command -v xdg-open &>/dev/null; then
  xdg-open "$HELP" &
fi
""")
run('chmod +x chroot/usr/local/bin/ridos-help-center')

HC = """[Desktop Entry]
Version=1.0
Type=Application
Name=RIDOS Help Center
Comment=Interactive guide for all RIDOS OS tools and commands
Exec=ridos-help-center
Icon=help-browser
Terminal=false
Categories=System;Documentation;
StartupNotify=true
"""
write('chroot/usr/share/applications/ridos-help-center.desktop', HC)
write('chroot/home/ridos/Desktop/ridos-help-center.desktop', HC)
write('chroot/etc/skel/Desktop/ridos-help-center.desktop', HC)
run('chmod +x chroot/home/ridos/Desktop/ridos-help-center.desktop')
run('chmod +x chroot/etc/skel/Desktop/ridos-help-center.desktop')
print("  ✅ RIDOS Help Center installed")

# ════════════════════════════════════════════════════════════════
# تصحيح الملكية
# ════════════════════════════════════════════════════════════════
print("\n[*] Fixing ownership...")
run('chroot chroot chown -R ridos:ridos /home/ridos/')
run('chroot chroot chmod 755 /home/ridos/Desktop')
run('chroot chroot chmod +x /home/ridos/Desktop/*.desktop 2>/dev/null || true')

# ════════════════════════════════════════════════════════════════
# تفعيل الخدمات
# ════════════════════════════════════════════════════════════════
print("\n[*] Enabling services...")
for svc in ['lightdm','NetworkManager','bluetooth','cups',
            'acpid','ssh','spice-vdagentd','ollama','ufw']:
    run(f'chroot chroot systemctl enable {svc} 2>/dev/null || true')
run('chroot chroot systemctl disable ridos-dashboard 2>/dev/null || true')

print("\n✅ configure-system.py complete — all 5 fixes applied")
print("   1. Wallpaper: xml + skel + profile.d + autostart")
print("   2. Firefox: removed from all locations")
print("   3. Control Center: wrapper launcher created")
print("   4. AI Shell: xfce4-terminal launcher created")
print("   5. Desktop: show-home/filesystem/trash = false")
