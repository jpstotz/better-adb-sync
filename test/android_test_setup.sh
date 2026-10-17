#!/system/bin/sh
set -eu

# Unicode examples for device paths: \u00fc -> ü, \u00df -> ß, \u263a -> ☺.
ROOT="/data/local/tmp/better_adb_sync_tests"
UMLAUT_DIR="äöü"
SMILEY="☺"

rm -rf "$ROOT"
mkdir -p "$ROOT/nested/empty" "$ROOT/nested/with_files" \
  "$ROOT/folder with spaces" \
  "$ROOT/folder with spaces/nested (with) [brackets] & plus+sign" \
  "$ROOT/with#hash!and+plus" \
  "$ROOT/emoji-$UMLAUT_DIR" \
  "$ROOT/folder with spaces/emoji-$SMILEY"

printf '%s' 'root file' > "$ROOT/root.txt"
printf '%s' 'nested file' > "$ROOT/nested/with_files/inner.txt"
printf '%s' 'hidden file' > "$ROOT/.hidden.txt"
printf '%s' 'space file' > "$ROOT/folder with spaces/space file.txt"
printf '%s' 'special file' > "$ROOT/folder with spaces/nested (with) [brackets] & plus+sign/special!file#1+plus.txt"
printf '%s' 'hash file' > "$ROOT/with#hash!and+plus/hash file.txt"
printf '%s' 'unicode file' > "$ROOT/emoji-$UMLAUT_DIR/$UMLAUT_DIR.txt"
printf '%s' 'smiley file' > "$ROOT/folder with spaces/emoji-$SMILEY/smiley-$SMILEY.txt"
