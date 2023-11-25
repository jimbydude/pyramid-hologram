#!/bin/bash
source ~/.bashrc
export TERM=xterm-256color
export DISPLAY=:0

# Navigate to the directory containing control.py (replace with the correct path)
cd /home/roseann/scripts

# Load user-specific bashrc to access setup_env
source ~/.bashrc

# Activate the virtual environment
source hologram/bin/activate

# Run control.py
python3 control.py
