import hashlib
import os
from tqdm import tqdm  # Progress bar
import nmap  # Nmap module for network scanning

# Load real malware hashes from a file
def load_malware_hashes(file_path):
    """
    Loads known malware hashes from a file.
    Each line in the file should contain one SHA-256 hash.
    """
    try:
        with open(file_path, "r") as f:
            return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        print(f"Error: Malware database file '{file_path}' not found.")
    except Exception as e:
        print(f"Error loading malware database: {e}")
    return set()

# Compute SHA-256 hash of a file
def get_sha256(file_path):
    """
    Calculates the SHA-256 hash of a file in chunks to optimize memory usage.
    """
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except PermissionError:
        print(f"Permission denied: {file_path}")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return None

# Scan directory and compare hashes
def scan_directory(directory, malware_hashes):
    """
    Recursively scans a directory for files, computes their SHA-256 hashes,
    and checks for matches with known malware hashes.
    """
    print(f"\nScanning directory: {directory}\n")
    
    # Count total files for progress bar
    total_files = sum(len(files) for _, _, files in os.walk(directory))
    if total_files == 0:
        print("No files found to scan.")
        return
    
    with tqdm(total=total_files, desc="Scanning", unit="file") as pbar:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = get_sha256(file_path)
                if file_hash:
                    print(f"Scanned: {file_path} | SHA-256: {file_hash}")
                    if file_hash in malware_hashes:
                        print(f"ALERT: Malware detected! {file_path}")
                pbar.update(1)

# Nmap Network Scanner
def nmap_scan(target_ip):
    """
    Scans the given target IP for open ports and running services using Nmap.
    """
    print(f"\nStarting Nmap scan on {target_ip}...\n")
    
    nm = nmap.PortScanner()
    nm.scan(target_ip, arguments='-sV')
    
    for host in nm.all_hosts():
        print(f"\nHost: {host} ({nm[host].hostname()})")
        print(f"State: {nm[host].state()}")
        
        for proto in nm[host].all_protocols():
            print(f"\nProtocol: {proto}")
            
            ports = nm[host][proto].keys()
            for port in sorted(ports):
                service = nm[host][proto][port]
                print(f"Port: {port}\tState: {service['state']}\tService: {service['name']}\tVersion: {service.get('version', 'N/A')}")
                
# Load malware hashes
malware_hashes = load_malware_hashes("malware_hashes.txt")

# Run the Nmap network scan
target_ip = "192.168.1.0/24"  # Change this to your local network range
nmap_scan(target_ip)

# Run the malware scanner
scan_directory("/Users/mohdmeraaz08/Documents/TDC/Cyber_security/Week4_minorProject", malware_hashes)
