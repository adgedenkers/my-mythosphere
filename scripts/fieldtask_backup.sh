#!/bin/bash
# Backup current fieldtask YAML to a timestamped copy before edits

TASK_FILE="fieldtasks/2025-08-02.yaml"
BACKUP_DIR="backups"

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

# Create backup copy with timestamp
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
cp "$TASK_FILE" "$BACKUP_DIR/2025-08-02_$TIMESTAMP.yaml"

echo "Backup of $TASK_FILE saved as $BACKUP_DIR/2025-08-02_$TIMESTAMP.yaml"