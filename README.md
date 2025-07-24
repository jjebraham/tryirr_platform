# Auto Update Script

This repository includes a helper script `update_repo.sh` that checks for updates
in the git repository, pulls them if present, restarts the application via
`supervisorctl`, and notifies a Telegram channel when an update occurs.

## Configuration

Edit the variables at the top of `update_repo.sh` to match your environment:

- `REPO_PATH` – path to the git repository
- `APP_NAME` – supervisor application name
- `MONITOR_BOT_TOKEN` – Telegram bot token
- `MONITOR_CHANNEL_ID` – channel or chat ID to post logs

## Cron Setup

Make the script executable and add it to your crontab so it runs every minute:

```bash
chmod +x /home/youruser/update_repo.sh
crontab -e
```

Add the following line:

```cron
* * * * * /home/youruser/update_repo.sh >> /home/youruser/update_log.txt 2>&1
```

This will log the output to `update_log.txt` and notify the configured Telegram
channel whenever the repository updates and the app is restarted.

## Database migrations

After modifying models you should generate and apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

The project uses SendGrid for email delivery. Set `SENDGRID_API_KEY` in your
environment before running the app.
