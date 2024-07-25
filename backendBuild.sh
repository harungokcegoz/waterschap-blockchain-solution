#!/bin/bash

if [[ "$OSTYPE" == "darwin"* ]]; then
    cd backend
    python3 build.py
elif [[ "$OSTYPE" == "win"* ]]; then
    cd backend
    python build.py
else
    echo "Unsupported operating system"
    exit 1
fi