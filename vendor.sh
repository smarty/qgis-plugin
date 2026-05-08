#!/usr/bin/env bash
# Updates the vendored Smarty SDK inside the plugin directory.
# Usage: ./vendor.sh
# After running, commit the updated smartystreets_python_sdk* directories.
set -euo pipefail

PLUGIN_DIR="smarty"

# Remove old vendored SDK artifacts
rm -rf "$PLUGIN_DIR/smartystreets_python_sdk"
rm -rf "$PLUGIN_DIR/smartystreets_python_sdk_version"
rm -rf "$PLUGIN_DIR"/smartystreets_python_sdk-*.dist-info

# Install SDK without transitive deps — requests is bundled with QGIS's Python
pip install -r requirements.txt --target "$PLUGIN_DIR" --no-deps --upgrade

# Remove bytecode cache that pip may have left behind
find "$PLUGIN_DIR" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find "$PLUGIN_DIR" -name "*.pyc" -delete 2>/dev/null || true

echo "Done. Commit the updated smartystreets_python_sdk* directories."
