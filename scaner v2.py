import socket
from concurrent.futures import ThreadPoolExecutor
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scan_port(ip, port, timeout=0.5):
    """Сканує окремий порт"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            return port, True
    except socket.timeout:
        logging.warning(f"Timeout occurred on port {port}.")
        return port, False
    except socket.error as e:
        logging.warning(f"Socket error on port {port}: {e}")
        return port, False

def scan_port_wrapper(port, ip, timeout):
    """Wrapper function for scan_port to improve readability"""
    return scan_port(ip, port, timeout)

def scan_ports(ip, start_port, end_port, timeout=0.5, max_workers=50):
    """Сканує діапазон портів"""
    logging.info(f"Scanning {ip} for open ports from {start_port} to {end_port}...")
    open_ports = (port for port, is_open in ThreadPoolExecutor(max_workers=max_workers).map(
        lambda port: scan_port_wrapper(port, ip, timeout), range(start_port, end_port + 1)) if is_open)

    found_ports = False
    for port in open_ports:
        found_ports = True
        logging.info(f"Port {port} is open!")

    if not found_ports:
        logging.info("No open ports found.")

if __name__ == "__main__":
    target_ip = input("Enter target IP address: ")
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))
    timeout = float(input("Enter timeout (seconds): "))
    max_workers = int(input("Enter the number of workers: "))
    scan_ports(target_ip, start_port, end_port, timeout, max_workers)
