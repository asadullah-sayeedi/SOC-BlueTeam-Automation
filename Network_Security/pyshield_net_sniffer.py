"""
════════════════════════════════════════════════════════════════════
PyShield-NetSniffer - Blue-Trace
════════════════════════════════════════════════════════════════════
 Copyright (c) 2026 Blue-Trace / Asadullah Sayeedi
 GitHub: https://github.com/Asadullah-SaYeedi/blue-trace
 LICENSE: MIT (see LICENSE file)
 DO NOT REMOVE THIS HEADER.
🔹 Description: Opens a raw socket to sniff network packets in real-time,
                decodes IPv4 headers, and logs packet flows.
════════════════════════════════════════════════════════════════════
"""



import socket
import struct
import sys

def start_sniffer():
    print("=" * 65)
    print(" 📡 PyShield-NetSniffer: RAW SOCKET INGESTION ENGINE ACTIVE 📡 ")
    print("=" * 65)

    try:
        # ایجاد سوکت خام برای دریافت تمام پکت‌های لایه شبکه (مخصوص لینوکس)
        sniffer = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    except PermissionError:
        print("[-] Error: You MUST run this script with ROOT privileges (sudo).")
        sys.exit(1)

    try:
        while True:
            raw_packet, addr = sniffer.recvfrom(65535)
            
            # پروتکل اترنت در ۱۴ بایت اول قرار دارد
            eth_header = raw_packet[:14]
            eth_data = struct.unpack("!6s6sH", eth_header)
            eth_protocol = socket.ntohs(eth_data[2])

            # بررسی اینکه آیا پکت از نوع IPv4 است (پروتکل 8)
            if eth_protocol == 8:
                ip_header = raw_packet[14:34]
                ip_data = struct.unpack("!BBHHHBBH4s4s", ip_header)
                
                # استخراج آی‌پي مبدأ و مقصد از پکت خام
                src_ip = socket.inet_ntoa(ip_data[8])
                dst_ip = socket.inet_ntoa(ip_data[9])
                
                print(f"[+] Traffic Flow: {src_ip} ──> {dst_ip}")
                
    except KeyboardInterrupt:
        print("\n[-] Sniffer stopped by user.")
        sys.exit(0)

if __name__ == "__main__":
    start_sniffer()
