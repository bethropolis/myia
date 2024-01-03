#!/bin/bash

# To run you have to give it permissions first
# --------------------------------------
# $ chmod +x install_chrome.sh
# $ ./install_chrome.sh
# --------------------------------------

# Check if Chrome is already installed
if ! dpkg -s google-chrome-stable >/dev/null 2>&1; then
  echo "Google Chrome is not installed. Installing..."

  sudo apt install libxss1 libappindicator1 libindicator7 -y

  curl -sO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

  sudo dpkg -i google-chrome-stable_current_amd64.deb

  sudo apt -f install -y

  rm google-chrome-stable_current_amd64.deb

  echo "Google Chrome has been installed successfully."
else
  echo "Google Chrome is already installed."
fi
