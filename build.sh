# Build the binary.
python -OO -m PyInstaller \
  --noconfirm \
  --console \
  --onefile \
  --distpath build/dist \
  --specpath build \
  snap_del.py

# Rename the binary.
if [[ -f build/dist/snap_del.exe ]]; then
  SNAP_DEL_BIN="build/dist/snap_del.exe"
else
  SNAP_DEL_BIN="build/dist/snap_del"
fi

# Generate the SHA256 checksum.
if [[ -x /usr/local/bin/gsha256sum ]]; then
  SHA256SUM_BIN=/usr/local/bin/gsha256sum
else
  SHA256SUM_BIN=sha256sum
fi
"$SHA256SUM_BIN" -b "$SNAP_DEL_BIN" | sed 's/ .*//g' > "$SNAP_DEL_BIN.sha256"
echo "sha256sum: $(cat "$SNAP_DEL_BIN.sha256") ($SNAP_DEL_BIN.sha256)"