#!/usr/bin/env bash
# python proxyPool.py server &
# python proxyPool.py schedule

SCRIPT_PATH="$(pwd $PATH)"

osascript 2>/dev/null <<EOF
    tell application "Terminal"
    activate
    do script "python $SCRIPT_PATH/proxyPool.py server"
    end tell
EOF

osascript 2>/dev/null <<EOF
    tell application "System Events"
      tell process "Terminal" to keystroke "t" using command down
    end
    tell application "Terminal"
      activate
      do script "python $SCRIPT_PATH/proxyPool.py schedule" in window 1
    end tell
EOF