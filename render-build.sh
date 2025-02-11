#!/bin/bash

# Enable error handling
set -e

# Update system and install Tesseract OCR
sudo apt update && sudo apt install -y tesseract-ocr

# Install Python dependencies from requirements.txt
pip install --no-cache-dir -r requirements.txt