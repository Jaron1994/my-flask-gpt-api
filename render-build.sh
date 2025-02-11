#!/bin/bash
set -e  # Stop on errors

# Create a directory for Tesseract
mkdir -p ~/tesseract

# Download a valid precompiled Tesseract binary for Linux
curl -L -o ~/tesseract/tesseract.zip "https://github.com/UB-Mannheim/tesseract/releases/download/v5.3.3/tesseract-ocr-linux.zip"

# Install unzip if it's not available
sudo apt update && sudo apt install -y unzip

# Extract the Tesseract binary
unzip ~/tesseract/tesseract.zip -d ~/tesseract

# Ensure the extracted binary is available in PATH
export PATH=$HOME/tesseract/bin:$PATH

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt
