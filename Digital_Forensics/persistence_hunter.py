"""
════════════════════════════════════════════════════════════════════
PyShield-PersistenceHunter - Blue-Trace
════════════════════════════════════════════════════════════════════
 Copyright (c) 2026 Blue-Trace / Asadullah Sayeedi
 GitHub: https://github.com/Asadullah-SaYeedi/blue-trace
 LICENSE: MIT (see LICENSE file)
 DO NOT REMOVE THIS HEADER.
🔹 Description: Scans the sensitive Windows Registry Run keys to discover
                hidden startup programs used by attackers for persistence.
════════════════════════════════════════════════════════════════════
"""




import os
import sys

def hunt_persistence():
    print("=" * 65)
    print(" 🎯 PyShield-PersistenceHunter: REGISTRY THREAT HUNTING ACTIVE 🎯 ")
    print("=" * 65)

    if os.name != 'nt':
        print("[-] Error: This forensic tool is specialized for Windows Registry environments only.")
        sys.exit(1)

    import winreg
    # مسیر کلید رجیستری معروف Run در ویندوز
    path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_READ)
        print(f"[*] Querying hive: HKEY_CURRENT_USER\\{path}\n")
        
        print(f"{'Registry Entry Name':<25} | {'Executable Path / Payload'}")
        print("-" * 65)
        
        for i in range(100):
            try:
                name, value, _ = winreg.EnumValue(key, i)
                print(f"{name:<25} | {value}")
            except OSError:
                break # اتمام لیست برنامه‌های استارت‌آپ
                
        winreg.CloseKey(key)
    except Exception as e:
        print(f"[-] Execution failure: {e}")
    print("=" * 65)

if __name__ == "__main__":
    hunt_persistence()
