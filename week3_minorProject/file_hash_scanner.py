import hashlib
import os

# Function to compute SHA-256 hash of a file
def get_sha256(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

# Function to scan a directory
def scan_directory(directory):
    malicious_hashes = {"5d41402abc4b2a76b9719d911017c592"}  # Example malicious hash
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = get_sha256(file_path)
            if file_hash:
                print(f"File: {file_path} | SHA-256: {file_hash}")
                if file_hash in malicious_hashes:
                    print(f"⚠️ ALERT: Suspicious file detected -> {file_path}")

# Run the scanner
scan_directory("/path/to/directory")  # Change this to the directory you want to scan
