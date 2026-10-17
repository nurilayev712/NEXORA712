"""
NEXORA DEV - Avtomatik WebApp Server va Cloudflare Tunnel
"""
import os
import re
import sys
import time
import subprocess
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

# Windows UTF-8 stdout
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent
WEBAPP_DIR = BASE_DIR / "webapp"
PORT = 8080


def run_http_server():
    """Lokal WebApp HTTP serverini yoqish"""
    os.chdir(str(WEBAPP_DIR))
    server = HTTPServer(("127.0.0.1", PORT), SimpleHTTPRequestHandler)
    print(f"[*] Mahalliy WebApp server 127.0.0.1:{PORT} da ishga tushdi.", flush=True)
    server.serve_forever()


def update_env_url(tunnel_url: str):
    """bot/.env fayliga yangi HTTPS havolani yozish"""
    env_file = BASE_DIR / "bot" / ".env"
    if not env_file.exists():
        env_file = BASE_DIR / ".env"

    try:
        content = env_file.read_text(encoding="utf-8")
        if "WEBAPP_URL=" in content:
            content = re.sub(r"WEBAPP_URL=.*", f"WEBAPP_URL={tunnel_url}", content)
        else:
            content += f"\nWEBAPP_URL={tunnel_url}\n"
        env_file.write_text(content, encoding="utf-8")
        print(f"[+] .env fayliga yangi WEBAPP_URL yozildi: {tunnel_url}", flush=True)
    except Exception as e:
        print(f"[-] .env faylini yangilashda xatolik: {e}", flush=True)


def run_tunnel():
    """Cloudflared Quick Tunnel ni ishga tushirish"""
    cmd = ["cloudflared", "tunnel", "--url", f"http://127.0.0.1:{PORT}"]
    print("[*] Cloudflare Tunnel ishga tushirilmoqda...", flush=True)

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    tunnel_url = None
    url_pattern = re.compile(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com")

    while True:
        line = process.stdout.readline()
        if not line:
            break
        match = url_pattern.search(line)
        if match and not tunnel_url:
            tunnel_url = match.group(0)
            print("\n" + "=" * 60, flush=True)
            print(f"[SUCCESS] TAYYOR! CLOUDFLARE WEBAPP HAVOLASI: {tunnel_url}", flush=True)
            print("=" * 60 + "\n", flush=True)
            update_env_url(tunnel_url)
            try:
                subprocess.run([sys.executable, str(BASE_DIR / "update_menu_button.py")], check=False)
            except Exception as e:
                print(f"[-] update_menu_button xatolik: {e}", flush=True)

    process.wait()


if __name__ == "__main__":
    # 1. HTTP serverni alohida threadda yoqish
    server_thread = threading.Thread(target=run_http_server, daemon=True)
    server_thread.start()
    time.sleep(1)

    # 2. Cloudflare tunnelni yoqish
    run_tunnel()
