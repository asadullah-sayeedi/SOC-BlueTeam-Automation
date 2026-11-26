# 🛡️ SOC & Blue Team Security Automation Toolkit

Welcome to my Cyber Security Portfolio. This repository contains a collection of enterprise-grade Python scripts designed for **SOC Analysts (Tier 1/2/3)**, **Threat Hunters**, and **Incident Responders** to automate detection, forensic acquisition, and host isolation.

---

## 📊 Project Matrix & Capabilities

Below is the complete structural breakdown of the defensive security tools implemented in this repository, mapped to industry use cases:

| # | Folder Name | Script Name | Target OS | Primary Tactic / Goal | Key Technical Capabilities |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | `Linux_Defense` | `pyshield_soc_linux.py` | 🐧 Linux | Incident Response & Active Defense | Parses `auth.log` for SSH Brute Force, enforces real-time **IPTables** blocking, and seals evidence via SHA-256. |
| **02** | `Windows_Defense` | `pyshield_soc_windows.py` | 🪟 Windows | Incident Response & Mitigation | Monitors Event ID 4625 via live PowerShell pipe, dynamically invokes **Windows Advanced Firewall** rules (`netsh`) to block attackers. |
| **03** | `Network_Security` | `pyshield_net_sniffer.py` | 🐧 Linux | Threat Hunting & Monitoring | Opens Raw Sockets (`AF_PACKET`) to sniff live traffic and decode IPv4/TCP headers looking for malicious vectors. |
| **04** | `Digital_Forensics`| `forensic_artifact_dump.py`| Multi-OS | Digital Forensics & Incident Response| Extracts live network state artifacts (`netstat`/`ss`), dumps active socket telemetry, and generates a strict cryptographic seal. |
| **05** | `Digital_Forensics`| `persistence_hunter.py` | 🪟 Windows | Threat Hunting & Evasion Detection | Programmatically queries sensitive Windows Registry Run keys (`HKCU\...\Run`) to hunt for hidden malware persistence. |

---

## 🛠️ How to Deploy & Simulate in Your Lab

### 1. Prerequisites
Ensure you run these scripts with elevated/administrative privileges since they interact directly with kernel-level firewalls and network interfaces.
* On Linux: Use `sudo`
* On Windows: Open CMD / PowerShell as **Run as Administrator**

### 2. Running Windows Tools (Firewall & Registry Hunt)
```cmd
# Navigate to the directory and execute with Administrator privileges:
python Windows_Defense/pyshield_soc_windows.py
python Digital_Forensics/persistence_hunter.py
```

### 3. Running Linux Tools (IPTables Defense & Sniffer)
```bash
# Execute the live defense and monitoring scripts:
sudo python3 Linux_Defense/pyshield_soc_linux.py
sudo python3 Network_Security/pyshield_net_sniffer.py
```

## 🔒 Forensic Integrity & Preserving Evidence
Every tool in this toolkit enforces the **Chain of Custody** protocol. Upon triggering a mitigation action or data dump, the scripts automatically calculate a SHA-256 cryptographic hash of the extracted metadata to ensure that digital evidence remains tamper-proof and judicially valid.

---
💡 *Developed by **Asadullah SaYeedi** | Cyber Security Analyst & Python Automation Specialist.*
