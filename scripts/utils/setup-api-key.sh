#!/bin/bash

# Secure API Key Setup Script
# This script helps you add your Gemini API key securely

echo "🔐 Secure API Key Setup"
echo "======================="
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
fi

echo "Please enter your Gemini API key:"
echo "(It should start with 'AIza...')"
echo ""
read -s GEMINI_KEY  # -s flag hides input for security

# Validate key format
if [[ ! $GEMINI_KEY =~ ^AIza ]]; then
    echo ""
    echo "⚠️  Warning: Your key doesn't start with 'AIza'"
    echo "   Are you sure this is a Gemini API key?"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 1
    fi
fi

# Update .env file
if grep -q "GEMINI_API_KEY=" .env; then
    # Replace existing key
    sed -i.bak "s/GEMINI_API_KEY=.*/GEMINI_API_KEY=$GEMINI_KEY/" .env
    echo "✅ Updated existing GEMINI_API_KEY in .env"
else
    # Add new key
    echo "GEMINI_API_KEY=$GEMINI_KEY" >> .env
    echo "✅ Added GEMINI_API_KEY to .env"
fi

# Set secure permissions
chmod 600 .env
echo "✅ Set secure permissions on .env (owner read/write only)"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Your API key is now securely stored in .env"
echo "The .env file is already in .gitignore (won't be committed to git)"
echo ""
echo "Next steps:"
echo "1. source venv/bin/activate"
echo "2. pip install -r requirements.txt"
echo "3. uvicorn src.api.main:app --reload"
echo ""
