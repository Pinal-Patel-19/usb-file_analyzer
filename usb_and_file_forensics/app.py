from flask import Flask, render_template, request
import os, psutil, hashlib, time

app = Flask(__name__)

# Load known malicious hashes from file
def load_malicious_hashes():
    if not os.path.exists("demo_suspicious_hashes.txt"):
        return set()
    hashes = set()
    with open("demo_suspicious_hashes.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip().lower()
            if not line or line.startswith("#"):
                continue
            hashes.add(line)
    return hashes

malicious_hashes = load_malicious_hashes()

# Scan all connected USB drives
def scan_usb_drives():
    usb_drives = []
    for partition in psutil.disk_partitions():
        if "removable" in partition.opts or "cdrom" in partition.device.lower():
            usb_drives.append(partition.mountpoint)
    return usb_drives

# Compute SHA256 hash of a file
def get_file_hash(file_path):
    try:
        with open(file_path, "rb") as f:
            file_hash = hashlib.sha256()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return file_hash.hexdigest()
    except Exception:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    usb_drives = scan_usb_drives()
    results = []

    if not usb_drives:
        return render_template('result.html', results=None, message="No USB drives detected!")

    for drive in usb_drives:
        for root, _, files in os.walk(drive):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = get_file_hash(file_path)
                if file_hash and file_hash in malicious_hashes:
                    results.append({
                        "file": file_path,
                        "hash": file_hash,
                        "status": "⚠️ Suspicious"
                    })
                elif file_hash:
                    results.append({
                        "file": file_path,
                        "hash": file_hash,
                        "status": "✅ Clean"
                    })
    return render_template('result.html', results=results, message=None)

if __name__ == "__main__":
    app.run(debug=True)
