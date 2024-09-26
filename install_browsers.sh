#!/bin/bash

# Update package list
echo "Updating package list..."
sudo apt-get update

# Install Google Chrome from Chrome for Testing
echo "Fetching the latest stable Chrome for Testing version..."
CHROME_URL=$(curl -sS "https://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone-with-downloads.json" | jq -r '.["115"].downloads.chrome[].url' | grep "linux64" | head -n 1)

# Download and install Chrome
echo "Downloading Chrome from $CHROME_URL"
wget $CHROME_URL -O google-chrome-stable_linux64.deb
sudo apt-get install -y ./google-chrome-stable_linux64.deb

# Clean up
rm google-chrome-stable_linux64.deb

# Get the version of Chrome installed
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+\.\d+' | head -1 | cut -d '.' -f 1-3)

# Install ChromeDriver that matches the Chrome version from CfT
echo "Fetching the latest ChromeDriver for version $CHROME_VERSION"
CHROME_DRIVER_URL=$(curl -sS "https://googlechromelabs.github.io/chrome-for-testing/latest-patch-versions-per-build-with-downloads.json" | jq -r --arg version "$CHROME_VERSION" '.[$version].downloads.chromedriver[].url' | head -1)

echo "Downloading ChromeDriver from $CHROME_DRIVER_URL"
wget $CHROME_DRIVER_URL -O chromedriver_linux64.zip
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
