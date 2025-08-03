# main.py

import argparse
import subprocess
import sys

def run_speak():
    """Run the voice assistant script."""
    subprocess.run([sys.executable, "speak.py"])

def run_chat():
    """Run the Flask web app."""
    subprocess.run([sys.executable, "chat.py"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run either the voice assistant or the web chat app.")
    parser.add_argument(
        "--mode",
        choices=["speak", "chat"],
        required=True,
        help="Choose which interface to run: 'speak' for voice assistant, 'chat' for web interface.",
    )
    args = parser.parse_args()

    if args.mode == "speak":
        run_speak()
    elif args.mode == "chat":
        run_chat()

        
# This script allows you to run either the voice assistant or the web chat app based on the command line argument provided.

# uv run main.py --mode speak

# uv run main.py --mode chat
