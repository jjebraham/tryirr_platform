#!/bin/bash

# Cron job script to auto-update the repository and restart the app,
# while posting the event to a Telegram channel.

# Configuration
REPO_PATH="/home/youruser/myrepo"
APP_NAME="myapp"
MONITOR_BOT_TOKEN="8126205777:AAFug3_WYIrvnX7bvVzCMnXvSFYaFvLyLI0"
MONITOR_CHANNEL_ID="-1002312817166"

cd "$REPO_PATH"

# Fetch new commits from origin
git fetch origin

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse @{u})

if [ "$LOCAL" != "$REMOTE" ]; then
    CHANGED_FILES=$(git diff --name-only HEAD..@{u} | xargs)
    if git pull && sudo supervisorctl restart "$APP_NAME"; then
        MESSAGE="Updated ${APP_NAME} with changes:%0A${CHANGED_FILES}"
        curl -s -X POST "https://api.telegram.org/bot${MONITOR_BOT_TOKEN}/sendMessage" \
             -d "chat_id=${MONITOR_CHANNEL_ID}" \
             -d "text=${MESSAGE}"
    else
        ERR="Update failed for ${APP_NAME}"
        curl -s -X POST "https://api.telegram.org/bot${MONITOR_BOT_TOKEN}/sendMessage" \
             -d "chat_id=${MONITOR_CHANNEL_ID}" \
             -d "text=${ERR}"
    fi
fi
