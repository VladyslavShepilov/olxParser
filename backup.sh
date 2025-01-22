#!/bin/bash

# Get current date for backup file name
BACKUP_DATE=$(date +%Y%m%d_%H%M%S)

# Create backup
pg_dump -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -F c -f "/backups/backup_${BACKUP_DATE}.dump"

# Keep only last 7 backups
cd /backups && ls -t | tail -n +8 | xargs -r rm --
