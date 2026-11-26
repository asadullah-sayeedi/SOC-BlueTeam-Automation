"""
════════════════════════════════════════════════════════════════════
  PyShield-Windows-SOC (Live Windows Security Log Monitor) - Blue-Trace
════════════════════════════════════════════════════════════════════
 Copyright (c) 2026 Blue-Trace / Asadullah Sayeedi
 GitHub: https://github.com/Asadullah-SaYeedi/blue-trace
 LICENSE: MIT (see LICENSE file)
 DO NOT REMOVE THIS HEADER.
🔹 Description: Queries live Windows Event Viewer for Event ID 4625 (Logon Failures)
                and automates mitigation via Windows Advanced Firewall.

════════════════════════════════════════════════════════════════════
"""
import os
import sys
import time
import hashlib
import subprocess
import re

FAILED_THRESHOLD = 5
failed_registry = {}

def is_admin():
    import ctypes
    return ctypes.windll.shell32.IsUserAnAdmin() != 0

def get_last_failed_logon():
    # ارتباط با پاورشل برای استخراج آخرین آی‌پی که تلاش ناموفق داشته است
    ps_cmd = 'Get-WinEvent -LogName Security -FilterHashtable @{LogName="Security";ID=4625} -MaxEvents 1 | Select-Object -ExpandProperty Message'
    proc = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True)
    
    if proc.returncode == 0 and proc.stdout:
        # پیدا کردن آی‌پی از داخل متن طولانی لاگ ویندوز
        ip_match = re.search(r"Source Network Address:\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", proc.stdout)
        if ip_match:
            return ip_match.group(1)
    return None

def monitor_windows_security():
    print("=" * 65)
    print(" 🔥 PyShield-Windows-SOC: LIVE EVENT VIEWER MONITOR ACTIVE 🔥 ")
    print("=" * 65)
    
    last_processed_ip = ""
    
    while True:
        current_failed_ip = get_last_failed_logon()
        
        # اگر لاگ جدیدی ثبت شده بود و آی‌پی معتبر بود
        if current_failed_ip and current_failed_ip != last_processed_ip and current_failed_ip != "127.0.0.1":
            last_processed_ip = current_failed_ip
            failed_registry[current_failed_ip] = failed_registry.get(current_failed_ip, 0) + 1
            print(f"[*] Detected Event ID 4625 from IP: {current_failed_ip} ({failed_registry[current_failed_ip]}/{FAILED_THRESHOLD})")
            
            if failed_registry[current_failed_ip] == FAILED_THRESHOLD:
                print(f"\n🚨 [CRITICAL] Windows Brute Force Confirmed from IP: {current_failed_ip}")
                
                # دستور واقعی فایروال ویندوز برای بلاک کردن آی‌پی
                rule_name = f"PyShield_Block_{int(time.time())}"
                fw_cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=block protocol=ANY remoteip={current_failed_ip}'
                subprocess.run(fw_cmd, shell=True, stdout=subprocess.DEVNULL)
                print(f"⛔ [WINDOWS FIREWALL] Created Rule '{rule_name}' to BLOCK IP: {current_failed_ip}")
                
                # پلمپ شواهد دیجیتال
                report = f"Windows_IP:{current_failed_ip}|Event:4625|Mitigation:Blocked"
                report_hash = hashlib.sha256(report.encode()).hexdigest()
                print(f"🔒 [FORENSICS] Seal (SHA-256): {report_hash}\n")
                
        time.sleep(2) # هر ۲ ثانیه یک‌بار Event Viewer را اسکن می‌کند

if __name__ == "__main__":
    if not is_admin():
        print("[-] Error: You MUST run this script as Administrator (Run as Administrator).")
        sys.exit(1)
    monitor_windows_security()
