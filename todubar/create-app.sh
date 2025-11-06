#!/bin/bash
# Create macOS Application Bundle for Todubar

set -e

APP_NAME="Todubar"
APP_DIR="$HOME/Applications/$APP_NAME.app"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Creating $APP_NAME.app in ~/Applications..."

# Create app bundle structure
mkdir -p "$APP_DIR/Contents/MacOS"
mkdir -p "$APP_DIR/Contents/Resources"

# Create Info.plist
cat > "$APP_DIR/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>Todubar</string>
    <key>CFBundleDisplayName</key>
    <string>Todubar</string>
    <key>CFBundleIdentifier</key>
    <string>com.todu.todubar</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>CFBundleExecutable</key>
    <string>Todubar</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>LSUIElement</key>
    <true/>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF

# Create launcher script
cat > "$APP_DIR/Contents/MacOS/$APP_NAME" << EOF
#!/bin/bash
# Todubar launcher script

cd "$SCRIPT_DIR"
exec "$SCRIPT_DIR/app.py"
EOF

chmod +x "$APP_DIR/Contents/MacOS/$APP_NAME"

echo "✓ Created $APP_NAME.app"
echo "✓ Location: $APP_DIR"
echo ""
echo "To launch:"
echo "  open ~/Applications/$APP_NAME.app"
echo ""
echo "To add to Login Items:"
echo "  1. Open System Settings → General → Login Items"
echo "  2. Click '+' under 'Open at Login'"
echo "  3. Navigate to ~/Applications and select $APP_NAME.app"
