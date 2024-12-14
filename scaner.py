import socket
from concurrent.futures import ThreadPoolExecutor

def scan_port(ip, port):
    """Сканує окремий порт"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            s.connect((ip, port))
            return port, True
    except:
        return port, False

def scan_ports(ip, start_port, end_port):
    """Сканує діапазон портів"""
    print(f"Scanning {ip} for open ports from {start_port} to {end_port}...")
    open_ports = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(lambda p: scan_port(ip, p), range(start_port, end_port + 1))
        for port, is_open in results:
            if is_open:
                open_ports.append(port)
                print(f"[+] Port {port} is open!")
    if not open_ports:
        print("[-] No open ports found.")
    else:
        print(f"\nOpen ports: {open_ports}")

if __name__ == "__main__":
    target_ip = input("Enter target IP address: ")
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))
    scan_ports(target_ip, start_port, end_port)
