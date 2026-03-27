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
# 8. تفعيل الخدمات
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
