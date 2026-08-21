import subprocess
import time
import re
import sys
import os

# Ensure clean UTF-8 stdout
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def start_system():
    print("=" * 65)
    print("MENTORBEE - PUBLIC SECURE CLOUD TUNNEL LAUNCHER")
    print("=" * 65)
    
    # 1. Run bootstrap
    print("[1/3] Verifying database and coordinator accounts...")
    subprocess.run([sys.executable, "bootstrap.py"], check=True)
    
    # 2. Check cloudflared.exe
    cloudflared_path = os.path.join(os.path.dirname(__file__), "cloudflared.exe")
    if not os.path.exists(cloudflared_path):
        print("\n[!] cloudflared.exe not found in directory.")
        return

    # 3. Start Uvicorn Server in background if not already running
    print("\n[2/3] Starting FastAPI Application Server (Port 8000)...")
    server_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(2)

    # 4. Start Cloudflare Tunnel
    print("\n[3/3] Establishing Secure Cloudflare Tunnel...")
    tunnel_proc = subprocess.Popen(
        [cloudflared_path, "tunnel", "--url", "http://127.0.0.1:8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        encoding="utf-8",
        errors="replace"
    )

    public_url = None
    start_time = time.time()
    while time.time() - start_time < 30:
        line = tunnel_proc.stdout.readline()
        if not line:
            continue
        # Look for trycloudflare.com link
        match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
        if match:
            public_url = match.group(0)
            break

    if public_url:
        print("\n" + "=" * 65)
        print(">>> YOUR LIVE PUBLIC HOSTED APP IS NOW ONLINE! <<<")
        print("=" * 65)
        print(f"\n[LIVE LINK] Public HTTPS URL: {public_url}")
        print(f"[PORTAL]    Mentor Home:      {public_url}/")
        print(f"[AUTH]      Mentor Login:     {public_url}/mentor/login")
        print(f"[ADMIN]     Admin Login:      {public_url}/admin")
        print(f"[DASHBOARD] Admin Dashboard:  {public_url}/admin/dashboard")
        print("\n" + "-" * 65)
        print("Default Credentials:")
        print("  - Universal Staff Passcode: AGENTBEE0809")
        print("  - Super Admin Login: admin@mentorbee.com / AdminPassword@123")
        print("=" * 65)
        print("\n[Keep this process running to maintain the live public tunnel.]")
        sys.stdout.flush()
    else:
        print("\n[!] Could not parse tunnel URL. Cloudflare output logs:")
        for _ in range(10):
            line = tunnel_proc.stdout.readline()
            if line:
                print("   ", line.strip())

    try:
        tunnel_proc.wait()
    except KeyboardInterrupt:
        print("\nStopping services...")
        tunnel_proc.terminate()
        server_proc.terminate()
        print("All services stopped.")

if __name__ == "__main__":
    start_system()
