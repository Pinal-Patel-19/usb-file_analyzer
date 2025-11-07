# USB Forensics & Suspicious File Detector

Simple Flask app that scans connected removable drives and compares file SHA-256 hashes against a local list (`demo_suspicious_hashes.txt`). 

## Setup (Windows)

1. Install Python 3.8+ and add to PATH.
2. Create & activate venv:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:

   ```bash
   python app.py
   ```

5. Open http://127.0.0.1:5000

## Notes
- Update `demo_suspicious_hashes.txt` with SHA-256 hashes (one per line) to flag files.
- This is a demo tool for educational purposes only.
