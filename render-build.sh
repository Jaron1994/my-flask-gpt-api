#!/bin/bash
set -e  # Stop on errors

# Download and extract a prebuilt Tesseract binary
mkdir -p ~/tesseract
curl -L -o ~/tesseract/tesseract.tar.gz https://github.com/tesseract-ocr/tesseract/releases/download/5.3.3/tesseract-5.3.3-linux-x86_64.tar.gz
tar -xvzf ~/tesseract/tesseract.tar.gz -C ~/tesseract --strip-components=1
rm ~/tesseract/tesseract.tar.gz

# Ensure the extracted binary is available in PATH
export PATH=$HOME/tesseract/bin:$PATH

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt
