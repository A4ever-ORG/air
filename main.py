import subprocess
import sys

def run_bot():
    try:
        subprocess.run([sys.executable, 'bot.py'])
    except Exception as e:
        print(f"Error running bot.py: {e}")

if __name__ == "__main__":
    run_bot()