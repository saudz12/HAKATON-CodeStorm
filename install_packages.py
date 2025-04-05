#!/usr/bin/env python3
"""
Educational AI Agent - Package Installer

This script installs all required dependencies for the Educational AI Agent application.
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install all required packages for the Educational AI Agent."""
    print("Installing dependencies for Educational AI Agent...")
    
    # List of required packages
    required_packages = [
        'openai',          # OpenAI API client for guide mode
        'groq',            # Groq API client for QA mode
        'pypdf',           # PDF processing 
        'sentence-transformers',  # Text embeddings for PDF search
        'numpy',           # Numerical operations
        'langdetect',      # Language detection for multilingual support
        'fitz',            # PyMuPDF for PDF processing
        'serpapi',         # For web search functionality
        'pycryptodome',    # For any encryption needs
        'python-dotenv',   # For environment variable management
    ]
    
    # Optional packages that might be useful
    optional_packages = [
        'flask',           # For web interface if needed
        'streamlit',       # For quick dashboard creation
        'pandas',          # For data manipulation
        'matplotlib',      # For visualization
        'scikit-learn',    # For machine learning capabilities
    ]
    
    # Check if pip is available
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', '--version'])
    except subprocess.CalledProcessError:
        print("Error: pip is not installed or not working correctly.")
        sys.exit(1)
    
    # Install each required package
    for package in required_packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', package
            ])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError:
            print(f"Error: Failed to install {package}")
            sys.exit(1)
    
    # Ask if user wants to install optional packages
    install_optional = input("\nWould you like to install optional packages for extended functionality? (y/n): ").lower()
    if install_optional == 'y':
        for package in optional_packages:
            print(f"Installing optional package {package}...")
            try:
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', package
                ])
                print(f"Successfully installed {package}")
            except subprocess.CalledProcessError:
                print(f"Warning: Failed to install optional package {package}")
    
    print("\nAll dependencies installed successfully!")
    print("\nTo use the Educational AI Agent, you'll need API keys for:")
    print("- OpenAI (for guide mode): https://platform.openai.com/")
    print("- Groq (for QA mode): https://console.groq.com/")
    print("- SerpAPI (for web search): https://serpapi.com/")
    print("\nYou can set these as environment variables:")
    print("export OPENAI_API_KEY='your-openai-key'")
    print("export GROQ_API_KEY='your-groq-key'")
    print("export SERP_API_KEY='your-serpapi-key'")
    
    # Ask if user wants to set API keys now
    set_keys = input("\nWould you like to set API keys now? (y/n): ").lower()
    if set_keys == 'y':
        openai_key = input("Enter your OpenAI API key (or press Enter to skip): ")
        groq_key = input("Enter your Groq API key (or press Enter to skip): ")
        serpapi_key = input("Enter your SerpAPI key (or press Enter to skip): ")
        
        if openai_key or groq_key or serpapi_key:
            # Create or append to .env file
            with open('.env', 'w') as f:
                if openai_key:
                    f.write(f"OPENAI_API_KEY={openai_key}\n")
                if groq_key:
                    f.write(f"GROQ_API_KEY={groq_key}\n")
                if serpapi_key:
                    f.write(f"SERP_API_KEY={serpapi_key}\n")
            
            print("\nAPI keys saved to .env file.")
            print("To load these in your session, run:")
            print("source .env  # For Unix/Linux/MacOS")
            print("or")
            print("set -a; source .env; set +a  # For some shells")
            print("or add them to your system environment variables for Windows")

if __name__ == "__main__":
    install_dependencies()