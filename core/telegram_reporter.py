import os
import urllib.request
import urllib.parse

BOT_TOKEN = os.getenv("MONITOR_BOT_TOKEN")
CHANNEL_ID = os.getenv("MONITOR_CHANNEL_ID")


def notify(message: str) -> None:
    """Send a message to the configured Telegram channel."""
    if not BOT_TOKEN or not CHANNEL_ID:
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": CHANNEL_ID, "text": message}).encode()
    try:
        urllib.request.urlopen(url, data=data, timeout=10)
    except Exception as exc:
        print("Failed to send Telegram notification:", exc)
