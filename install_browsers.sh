#!/bin/bash

# Update package list
echo "Updating package list..."
sudo apt-get update

# Install Google Chrome
echo "Installing Google Chrome..."
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt-get install -y ./google-chrome-stable_current_amd64.deb

# Clean up
rm google-chrome-stable_current_amd64.deb

# Get the version of Chrome installed
CHROME_VERSION=$(google-chrome --version | grep -oP '[\d.]+')

# Install ChromeDriver that matches the Chrome version
echo "Installing ChromeDriver..."
CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION)
wget https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip
sudo unzip chromedriver_linux64.zip -d /usr/local/bin
rm chromedriver_linux64.zip

# Install Firefox (alternative)
echo "Installing Firefox..."
sudo apt-get install -y firefox

# Install GeckoDriver (for Firefox)
echo "Installing GeckoDriver..."
GECKO_DRIVER_VERSION=$(curl -sS https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep 'tag_name' | cut -d '"' -f 4)
wget https://github.com/mozilla/geckodriver/releases/download/${GECKO_DRIVER_VERSION}/geckodriver-${GECKO_DRIVER_VERSION}-linux64.tar.gz
tar -xzf geckodriver-${GECKO_DRIVER_VERSION}-linux64.tar.gz
sudo mv geckodriver /usr/local/bin/
rm geckodriver-${GECKO_DRIVER_VERSION}-linux64.tar.gz

echo "Browser and driver installation complete."
