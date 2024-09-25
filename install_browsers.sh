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

# Verify Google Chrome installation
echo "Verifying Google Chrome installation..."
if command -v google-chrome &> /dev/null; then
    echo "Google Chrome installed successfully: $(google-chrome --version)"
else
    echo "Google Chrome installation failed."
    exit 1
fi

# Install ChromeDriver
echo "Installing ChromeDriver..."
CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip
sudo unzip chromedriver_linux64.zip -d /usr/local/bin
rm chromedriver_linux64.zip

# Verify ChromeDriver installation
echo "Verifying ChromeDriver installation..."
if [ -f /usr/local/bin/chromedriver ]; then
    echo "ChromeDriver installed successfully."
    ls -l /usr/local/bin/chromedriver  # Check permissions
else
    echo "ChromeDriver installation failed."
    exit 1
fi

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

# Verify GeckoDriver installation
echo "Verifying GeckoDriver installation..."
if [ -f /usr/local/bin/geckodriver ]; then
    echo "GeckoDriver installed successfully."
else
    echo "GeckoDriver installation failed."
    exit 1
fi

echo "Browser and driver installation complete."
