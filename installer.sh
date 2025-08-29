## ⚙️ installer.sh

#!/bin/bash
# Installer for Prime Advanced SQLi Scanner
# Works on Termux and Linux

echo "[*] Installing dependencies..."

# Update system
if [ -x "$(command -v apt)" ]; then
    apt update -y && apt upgrade -y
elif [ -x "$(command -v pkg)" ]; then
    pkg update -y && pkg upgrade -y
fi

# Install Python and pip
if [ -x "$(command -v pkg)" ]; then
    pkg install -y python git
else
    apt install -y python3 python3-pip git
fi

# Install required Python modules
pip install requests fake-useragent colorama

echo "✅ All requirements installed!"
echo "⚡ To run, use: python3 Dump.py"

echo "🕶 Ready to rule the shadows! 💀"
