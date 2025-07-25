import subprocess
import time
import urllib.request
import urllib.parse

# Monitor Bot for Logs
MONITOR_BOT_TOKEN = "8126205777:AAFug3_WYIrvnX7bvVzCMnXvSFYaFvLyLI0"
MONITOR_CHANNEL_ID = "-1002312817166"

REPO_PATH = "/home/youruser/myrepo"  # path to the git repository
APP_NAME = "myapp"  # your supervisor application name


def run(cmd, cwd=REPO_PATH):
    """Run a shell command and return its stdout as text."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)      
    return result.stdout.strip()


def notify(message: str) -> None:
    """Send a notification message to the monitoring Telegram channel."""
    url = f"https://api.telegram.org/bot{MONITOR_BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": MONITOR_CHANNEL_ID, "text": message}).encode()
    try:
        urllib.request.urlopen(url, data=data, timeout=10)
    except Exception as exc:
        print("Failed to send Telegram notification:", exc)


while True:
    # Update information about remote branches
    run("git fetch")

    # Get hashes for the local checked-out commit and its remote counterpart
    local_hash = run("git rev-parse @")
    remote_hash = run("git rev-parse '@{u}'")

    if local_hash != remote_hash:
        print("Update found. Pulling and restarting...")
        notify("Update found. Pulling latest changes...")
        run("git pull")
        run("python manage.py migrate --noinput")
        run("python manage.py collectstatic --noinput")
        subprocess.run(["sudo", "supervisorctl", "restart", APP_NAME])
        notify("✅ Deployed latest code: added Verification Center link, renamed to Peerexo, wallet USDT balance…")

    time.sleep(60)

