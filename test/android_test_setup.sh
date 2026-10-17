#!/system/bin/sh
set -eu

# Unicode examples for device paths: \u00fc -> ü, \u00df -> ß, \u263a -> ☺.
ROOT="/data/local/tmp/better_adb_sync_tests"
NORMAL_ROOT="$ROOT/normal"
PERMISSION_DENIED_ROOT="$ROOT/perm_denied"
UMLAUT_DIR="äöü"
SMILEY="☺"

rm -rf "$ROOT"
mkdir -p "$NORMAL_ROOT/nested/empty" "$NORMAL_ROOT/nested/with_files" \
  "$NORMAL_ROOT/folder with spaces" \
  "$NORMAL_ROOT/folder with spaces/nested (with) [brackets] & plus+sign" \
  "$NORMAL_ROOT/with#hash!and+plus" \
  "$NORMAL_ROOT/emoji-$UMLAUT_DIR" \
  "$NORMAL_ROOT/folder with spaces/emoji-$SMILEY"

printf '%s' 'root file' > "$NORMAL_ROOT/root.txt"
printf '%s' 'nested file' > "$NORMAL_ROOT/nested/with_files/inner.txt"
printf '%s' 'hidden file' > "$NORMAL_ROOT/.hidden.txt"
printf '%s' 'space file' > "$NORMAL_ROOT/folder with spaces/space file.txt"
printf '%s' 'special file' > "$NORMAL_ROOT/folder with spaces/nested (with) [brackets] & plus+sign/special!file#1+plus.txt"
printf '%s' 'hash file' > "$NORMAL_ROOT/with#hash!and+plus/hash file.txt"
printf '%s' 'nbsp file' > "$NORMAL_ROOT/folder with spaces/nbsp file.txt"
printf '%s' 'unicode file' > "$NORMAL_ROOT/emoji-$UMLAUT_DIR/$UMLAUT_DIR.txt"
printf '%s' 'smiley file' > "$NORMAL_ROOT/folder with spaces/emoji-$SMILEY/smiley-$SMILEY.txt"

mkdir -p "$PERMISSION_DENIED_ROOT/a_accessible_dir" \
  "$PERMISSION_DENIED_ROOT/b_blocked_dir" \
  "$PERMISSION_DENIED_ROOT/c_accessible_dir"

printf '%s' 'root accessible A' > "$PERMISSION_DENIED_ROOT/a_accessible.txt"
printf '%s' 'root blocked B' > "$PERMISSION_DENIED_ROOT/b_blocked.txt"
chmod 000 "$PERMISSION_DENIED_ROOT/b_blocked.txt"
printf '%s' 'root accessible C' > "$PERMISSION_DENIED_ROOT/c_accessible.txt"

printf '%s' 'dir accessible A' > "$PERMISSION_DENIED_ROOT/a_accessible_dir/a_accessible.txt"
printf '%s' 'dir blocked B' > "$PERMISSION_DENIED_ROOT/a_accessible_dir/b_blocked.txt"
chmod 000 "$PERMISSION_DENIED_ROOT/a_accessible_dir/b_blocked.txt"
printf '%s' 'dir accessible C' > "$PERMISSION_DENIED_ROOT/a_accessible_dir/c_accessible.txt"

mkdir -p "$PERMISSION_DENIED_ROOT/a_accessible_dir/nested" \
  "$PERMISSION_DENIED_ROOT/c_accessible_dir/nested"
printf '%s' 'nested accessible A' > "$PERMISSION_DENIED_ROOT/a_accessible_dir/nested/a_accessible.txt"
printf '%s' 'nested blocked B' > "$PERMISSION_DENIED_ROOT/a_accessible_dir/nested/b_blocked.txt"
chmod 000 "$PERMISSION_DENIED_ROOT/a_accessible_dir/nested/b_blocked.txt"
printf '%s' 'nested accessible C' > "$PERMISSION_DENIED_ROOT/a_accessible_dir/nested/c_accessible.txt"

printf '%s' 'dir accessible A' > "$PERMISSION_DENIED_ROOT/c_accessible_dir/a_accessible.txt"
printf '%s' 'dir blocked B' > "$PERMISSION_DENIED_ROOT/c_accessible_dir/b_blocked.txt"
chmod 000 "$PERMISSION_DENIED_ROOT/c_accessible_dir/b_blocked.txt"
printf '%s' 'dir accessible C' > "$PERMISSION_DENIED_ROOT/c_accessible_dir/c_accessible.txt"

printf '%s' 'nested accessible A' > "$PERMISSION_DENIED_ROOT/c_accessible_dir/nested/a_accessible.txt"
printf '%s' 'nested blocked B' > "$PERMISSION_DENIED_ROOT/c_accessible_dir/nested/b_blocked.txt"
chmod 000 "$PERMISSION_DENIED_ROOT/c_accessible_dir/nested/b_blocked.txt"
printf '%s' 'nested accessible C' > "$PERMISSION_DENIED_ROOT/c_accessible_dir/nested/c_accessible.txt"

chmod 000 "$PERMISSION_DENIED_ROOT/b_blocked_dir"
