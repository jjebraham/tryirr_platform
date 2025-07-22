import os
import re
import subprocess
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

try:
    from telegram import Bot
except Exception:
    Bot = None  # telegram not installed in dev

LOG_FILE = Path(settings.BASE_DIR) / 'auto_update.log'

class Command(BaseCommand):
    help = 'Check for git updates and deploy automatically.'

    def run(self, cmd):
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=settings.BASE_DIR)
        return result.stdout.strip()

    def handle(self, *args, **options):
        self.run('git fetch')
        changed_files = self.run('git diff --name-only origin/master..HEAD')
        if not changed_files:
            return
        diff_output = self.run('git diff origin/master..HEAD')
        added = re.findall(r'^\+def (\w+)', diff_output, re.MULTILINE)
        removed = re.findall(r'^-def (\w+)', diff_output, re.MULTILINE)
        summary = (
            f"Files changed: {changed_files}\n"
            f"Added functions: {', '.join(added) if added else 'none'}\n"
            f"Removed functions: {', '.join(removed) if removed else 'none'}"
        )
        with open(LOG_FILE, 'a') as log:
            log.write(summary + '\n')
        self.run('git pull')
        self.run('python manage.py migrate --noinput')
        self.run('python manage.py collectstatic --noinput')
        self.run('supervisorctl restart tryirr_platform')
        token = os.environ.get('TELEGRAM_BOT_TOKEN')
        chat_id = os.environ.get('TELEGRAM_CHAT_ID')
        if Bot and token and chat_id:
            Bot(token).send_message(chat_id=chat_id, text=summary + '\nRestarted.')
