#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="$(dirname "${BASH_SOURCE[0]}")/../test/diagrams"
OVERWRITE=false

# Parse arguments
for arg in "$@"; do
    if [[ "$arg" == "--overwrite" ]]; then
        OVERWRITE=true
    else
        echo "Unknown argument: $arg" >&2
        exit 1
    fi
done

# Iterate over all .tex files (excluding .expected.tex)
for src_file in "$SOURCE_DIR"/*.tex; do
    [[ "$src_file" == *.expected.tex ]] && continue

    base_name=$(basename "$src_file" .tex)
    target_file="$SOURCE_DIR/$base_name.expected.tex"

    if [[ "$OVERWRITE" == true || ! -f "$target_file" ]]; then
        cp "$src_file" "$target_file"
        echo "Copied: $src_file -> $target_file"
    else
        echo "Skipped (already exists): $target_file"
    fi
done
