"""
════════════════════════════════════════════════════════════════════
 PyShield-SOC (Real-time Linux Log Parser & Active Defense) - Blue-Trace
════════════════════════════════════════════════════════════════════
 Copyright (c) 2026 Blue-Trace / Asadullah Sayeedi
 GitHub: https://github.com/Asadullah-SaYeedi/blue-trace
 LICENSE: MIT (see LICENSE file)
 DO NOT REMOVE THIS HEADER.
🔹 Description: Parses live /var/log/auth.log for SSH Brute Force attacks
                and blocks the attacker IP instantly via IPTables.
════════════════════════════════════════════════════════════════════
"""


import os
import re
import time
import sys
import hashlib

LOG_FILE = "/var/log/auth.log"
FAILED_THRESHOLD = 5
failed_registry = {}

def monitor_linux_logs():
    print("=" * 65)
    print(" 🔥 PyShield-SOC: REAL-TIME LINUX DEFENSE ENGINE ACTIVE 🔥 ")
    print("=" * 65)
    
    if not os.path.exists(LOG_FILE):
        print(f"[-] Error: System log file '{LOG_FILE}' not found. Make sure SSH is enabled.")
        sys.exit(1)
        
    # باز کردن فایل و رفتن به انتهای آن برای خواندن لاگ‌های جدید
    with open(LOG_FILE, "r") as f:
        f.seek(0, 2)
        
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5) # منتظر لاگ جدید می‌ماند
                continue
                
            if "Failed password" in line:
                # استخراج آی‌پی با ساختار رنکس دقیق
                match = re.search(r"from\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", line)
                if match:
                    attacker_ip = match.group(1)
                    failed_registry[attacker_ip] = failed_registry.get(attacker_ip, 0) + 1
                    print(f"[*] Failed attempt from {attacker_ip} ({failed_registry[attacker_ip]}/{FAILED_THRESHOLD})")
                    
                    if failed_registry[attacker_ip] == FAILED_THRESHOLD:
                        print(f"\n🚨 [CRITICAL ALERT] SSH Brute Force Detected from: {attacker_ip}")
                        
                        # دستور واقعی مسدودسازی فایروال لینوکس
                        ban_cmd = f"sudo iptables -A INPUT -s {attacker_ip} -j DROP"
                        os.system(ban_cmd)
                        print(f"⛔ [IPTABLES] Blocked IP: {attacker_ip}")
                        
                        # ساخت سند جرم‌یابی دیجیتال
                        report = f"IP:{attacker_ip}|Attack:SSH_BruteForce|Status:Blocked"
                        report_hash = hashlib.sha256(report.encode()).hexdigest()
                        print(f"🔒 [FORENSICS] Cryptographic Seal (SHA-256): {report_hash}\n")

if __name__ == "__main__":
    if os.getuid() != 0:
        print("[-] Error: This script must be run with ROOT privileges (sudo python3 script.py).")
        sys.exit(1)
    monitor_linux_logs()
