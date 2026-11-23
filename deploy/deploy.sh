#!/usr/bin/env bash
# Update the site on our own server to the latest code.
# Usage (as root): bash /srv/tpt/app/deploy/deploy.sh
set -euo pipefail

APP=/srv/tpt/app
VENV=/srv/tpt/venv
ENV_FILE=/srv/tpt/.env

cd "$APP"
sudo -u tpt git pull --ff-only
sudo -u tpt "$VENV/bin/pip" install -q -r requirements.txt
sudo -u tpt bash -c "set -a; . '$ENV_FILE'; set +a
    '$VENV/bin/python' manage.py migrate --noinput
    '$VENV/bin/python' manage.py collectstatic --noinput"
systemctl restart tpt
echo "Deployed $(sudo -u tpt git log -1 --format='%h %s')"
