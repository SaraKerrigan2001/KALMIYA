import sys
import os
from pathlib import Path

# Setup paths
KALMIYA_DIR = Path(__file__).parent.parent / "01_systems" / "KALMIYA_System"
sys.path.insert(0, str(KALMIYA_DIR))

def test_telegram_clean():
    print("Testing Telegram Bot module cleanup...")
    from modules.telegram_bot import start_telegram_bot, TOKEN
    
    print(f"Loaded TOKEN value: {repr(TOKEN)}")
    assert TOKEN == "", f"Expected TOKEN to be empty, got {repr(TOKEN)}"
    
    # Try to start the bot
    result = start_telegram_bot()
    print(f"start_telegram_bot() returned: {result}")
    assert result is False, "Expected start_telegram_bot() to return False when TOKEN is empty/placeholder"
    print("✅ Telegram Bot cleanup test passed successfully!")

if __name__ == "__main__":
    test_telegram_clean()
