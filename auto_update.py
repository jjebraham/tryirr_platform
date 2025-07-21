import subprocess
import time

REPO_PATH = "/home/youruser/myrepo"  # path to the git repository
APP_NAME = "myapp"  # your supervisor application name


def run(cmd, cwd=REPO_PATH):
    """Run a shell command and return its stdout as text."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    return result.stdout.strip()


while True:
    # Update information about remote branches
    run("git fetch")

    # Get hashes for the local checked-out commit and its remote counterpart
    local_hash = run("git rev-parse @")
    remote_hash = run("git rev-parse '@{u}'")

    if local_hash != remote_hash:
        print("Update found. Pulling and restarting...")
        run("git pull")
        subprocess.run(["sudo", "supervisorctl", "restart", APP_NAME])

    time.sleep(60)
