"""
════════════════════════════════════════════════════════════════════
PyShield-ForensicDump - Blue-Trace
════════════════════════════════════════════════════════════════════
 Copyright (c) 2026 Blue-Trace / Asadullah Sayeedi
 GitHub: https://github.com/Asadullah-SaYeedi/blue-trace
 LICENSE: MIT (see LICENSE file)
 DO NOT REMOVE THIS HEADER.
🔹 Description: Collects live network connections, dumps them into an evidence file,
                and generates a cryptographic SHA-256 seal for judicial integrity.
════════════════════════════════════════════════════════════════════
"""



import subprocess
import hashlib
import time
import os

def collect_forensic_evidence():
    print("=" * 65)
    print(" 🔒 PyShield-ForensicDump: DIGITAL FORENSICS TRIAQE ACTIVE 🔒 ")
    print("=" * 65)

    evidence_dir = "Forensic_Output"
    if not os.path.exists(evidence_dir):
        os.makedirs(evidence_dir)

    timestamp = int(time.time())
    filename = f"{evidence_dir}/network_connections_{timestamp}.txt"

    # تعیین دستور متناسب با سیستم‌عامل برای جمع‌آوری شواهد زنده
    cmd = "netstat -ano" if os.name == "nt" else "ss -antp"
    print(f"[*] Running triage command: '{cmd}'...")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    # نوشتن شواهد درون فایل
    with open(filename, "w", encoding="utf-8") as f:
        f.write(result.stdout)
    print(f"[+] Live forensic artifacts successfully saved to: {filename}")

    # پلمپ دیجیتال فایل شواهد با هش برای تضمین عدم دستکاری (Integrity)
    hasher = hashlib.sha256()
    with open(filename, "rb") as f:
        hasher.update(f.read())
    evidence_hash = hasher.hexdigest()

    print("\n" + "-" * 65)
    print(f"📄 EVIDENCE FILE: {filename}")
    print(f"🔒 SHA-256 CRYPTOGRAPHIC SEAL: {evidence_hash}")
    print("-" * 65)
    print("[*] Record this hash in the Chain of Custody log sheet.\n")

if __name__ == "__main__":
    collect_forensic_evidence()
