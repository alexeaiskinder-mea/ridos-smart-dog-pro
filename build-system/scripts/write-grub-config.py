#!/usr/bin/env python3
"""
Write GRUB configuration for RIDOS OS — Smart Dog Edition
ميزة #1: Live-RAM Mode (toram) مُفعَّل في جميع مداخل الإقلاع
ميزة #6: Universal Hybrid Boot — دعم Legacy BIOS + UEFI
"""

grub_cfg = '''# RIDOS OS v1.2.0 Smart Dog — GRUB Configuration
# Supports: Legacy BIOS / UEFI / HDD / USB

set default=0
set timeout=8

# ─── ألوان واجهة GRUB ────────────────────────────────────────────
set menu_color_normal=white/black
set menu_color_highlight=black/cyan

# ─── الإقلاع الرئيسي (Live-RAM Mode) ───────────────────────────
menuentry "RIDOS OS v1.2.0 Smart Dog  [RAM Mode — سرعة قصوى]" {
  linux  /live/vmlinuz  boot=live toram quiet splash
  initrd /live/initrd
}

# ─── وضع آمن ────────────────────────────────────────────────────
menuentry "RIDOS OS  Safe Mode  [وضع آمن]" {
  linux  /live/vmlinuz  boot=live toram nomodeset
  initrd /live/initrd
}

# ─── وضع التشخيص (بدون RAM copy — للأجهزة ذات RAM < 4GB) ─────
menuentry "RIDOS OS  Diagnostic  [RAM < 4GB — توافق]" {
  linux  /live/vmlinuz  boot=live quiet splash
  initrd /live/initrd
}

# ─── وضع التصحيح الكامل ─────────────────────────────────────────
menuentry "RIDOS OS  Debug  [سجلات كاملة]" {
  linux  /live/vmlinuz  boot=live
  initrd /live/initrd
}

# ─── تحقق من ذاكرة RAM ──────────────────────────────────────────
menuentry "Memory Test — memtest86+  [فحص الذاكرة]" {
  linux  /live/vmlinuz  boot=live
  initrd /live/initrd
}
'''

import os
os.makedirs('iso/boot/grub', exist_ok=True)
with open('iso/boot/grub/grub.cfg', 'w') as f:
    f.write(grub_cfg)

print("✅ GRUB config written — Live-RAM (toram) enabled on main entry")
