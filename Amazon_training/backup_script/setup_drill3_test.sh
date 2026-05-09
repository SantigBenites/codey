#!/bin/bash
# setup_drill3_test.sh
# Creates a complete test environment for the backup script drill.
# Run this once, then point your backup script at:
#   source:      ./drill3_test/source_data
#   destination: ./drill3_test/backups

set -e

ROOT="./drill3_test"
SRC="$ROOT/source_data"
DEST="$ROOT/backups"

# Wipe any previous run
rm -rf "$ROOT"
mkdir -p "$SRC/config" "$SRC/logs" "$SRC/data" "$SRC/nested/deep/folder"
mkdir -p "$DEST"

# --- Source content ---
cat > "$SRC/config/app.conf" <<'EOF'
database_url=postgres://localhost:5432/mydb
log_level=INFO
max_connections=100
EOF

cat > "$SRC/config/secrets.env" <<'EOF'
API_KEY=sk-fake-key-12345
SECRET_TOKEN=abcdef123456
EOF

for i in $(seq 1 50); do
  echo "2026-05-08T$(printf '%02d' $((i % 24))):00:00Z INFO Log entry number $i" \
    >> "$SRC/logs/app.log"
done

echo '{"users": [{"id": 1, "name": "alice"}, {"id": 2, "name": "bob"}]}' \
  > "$SRC/data/users.json"

cat > "$SRC/data/contacts.csv" <<'EOF'
id,name,email
1,Alice,alice@example.com
2,Bob,bob@example.com
EOF

# Larger random file so the archive isn't trivially small
head -c 100000 /dev/urandom | base64 > "$SRC/data/blob.txt"

echo "deeply nested file" > "$SRC/nested/deep/folder/secret.txt"
echo "readme content"     > "$SRC/README.md"
touch                       "$SRC/empty.txt"
echo "spaces are tricky"  > "$SRC/file with spaces.txt"

# --- Pre-existing old backups (to test retention) ---
# Create 9 fake old backups with timestamps in the filename.
# After your script runs once, you should have at most 7 backups remaining.
for days_ago in 9 8 7 6 5 4 3 2 1; do
  ts=$(date -u -d "$days_ago days ago" +"%Y%m%dT%H%M%SZ" 2>/dev/null \
       || date -u -v-${days_ago}d +"%Y%m%dT%H%M%SZ")
  fake_archive="$DEST/backup_${ts}.tar.gz"
  # Make them real (valid) tar.gz files so verification logic doesn't trip
  tar -czf "$fake_archive" -C "$SRC" . 2>/dev/null
  # Set their mtime to match the simulated date
  touch -d "$days_ago days ago" "$fake_archive" 2>/dev/null \
    || touch -t "$(date -u -v-${days_ago}d +%Y%m%d%H%M)" "$fake_archive"
done

echo "=== Test environment ready ==="
echo ""
echo "Source:      $SRC"
echo "Destination: $DEST"
echo ""
echo "Source files:"
find "$SRC" -type f | sort | sed 's/^/  /'
echo ""
echo "Pre-existing backups (9 total — your script should prune to 7):"
ls -lt "$DEST" | tail -n +2 | sed 's/^/  /'
echo ""
echo "Now run your backup script:"
echo "  python backup.py $SRC $DEST"