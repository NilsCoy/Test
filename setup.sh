#!/bin/bash

echo "Installing system dependencies..."

sudo apt-get update

sudo apt-get install -y \
    ffmpeg \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libgtk-3-0

echo "Installing Python dependencies..."

pip install -r requirements.txt

echo "Installing Playwright browsers..."

playwright install --with-deps

echo "Done!"