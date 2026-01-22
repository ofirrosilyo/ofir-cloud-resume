#!/bin/bash

# Define paths
BACKUP_DIR="/mnt/k3s-backups"
K3S_DB_DIR="/var/lib/rancher/k3s/server/db"
K3S_TOKEN="/var/lib/rancher/k3s/server/token"
TIMESTAMP=$(date +"%Y-%m-%d_%H%M%S")
DESTINATION="$BACKUP_DIR/backup_$TIMESTAMP"

# Create a timestamped folder on the NAS
mkdir -p "$DESTINATION"

# Copy the database and the cluster token
echo "Starting K3s backup to $DESTINATION..."
cp -r "$K3S_DB_DIR" "$DESTINATION/"
cp "$K3S_TOKEN" "$DESTINATION/"

# Clean up backups older than 7 days on the NAS to save space
find "$BACKUP_DIR" -type d -name "backup_*" -mtime +7 -exec rm -rf {} +

echo "Backup completed successfully."
