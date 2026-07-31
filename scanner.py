import nmap
import socket

def get_local_subnet():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip.rsplit('.', 1)[0] + ".0/24"


def scan_network():
    nm = nmap.PortScanner()
    devices = []

    subnet = get_local_subnet()
    print(f"Scanning: {subnet}")

    nm.scan(subnet, arguments="-sn")

    for host in nm.all_hosts():
        ip = host
        mac = nm[host]['addresses'].get('mac', 'Unknown')
        vendor = nm[host]['vendor'].get(mac, 'Unknown')

        devices.append({
            "ip": ip,
            "mac": mac,
            "vendor": vendor,
            "os": "Unknown"
        })

    return devices
