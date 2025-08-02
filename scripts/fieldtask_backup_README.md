# Field Task Backup Script

This script creates a timestamped backup of the `2025-08-02.yaml` field task file.

## What It Does
- Ensures a `backups/` directory exists in your repo
- Copies the current field task YAML file to that directory
- Appends a timestamp to the backup filename for traceability

## Usage
Run from the root of the repo:
```bash
bash scripts/fieldtask_backup.sh
```

## Why Use This?
To prevent accidental overwrites or data loss when editing your field task YAML file during live updates.

Backups are lightweight and safely versioned, and this structure sets the foundation for future automation or database syncing.