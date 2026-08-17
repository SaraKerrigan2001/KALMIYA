import sys
sys.path.insert(0, r'c:\Users\maria\env\KALMIYA_System')
from security_ops import scan_network

devices = scan_network()
print("\n=== COMPLETE DEVICE LIST ===")
for d in devices:
    print(f"IP: {d['ip']} | Hostname: {d['hostname']} | MAC: {d.get('mac', 'N/A')} | Vendor: {d.get('vendor', 'N/A')}")
