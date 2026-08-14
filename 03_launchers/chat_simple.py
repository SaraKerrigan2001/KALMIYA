"""
Launcher para Chat KALMIYA Simple (tkinter puro)
"""
import sys
import os

workspace = os.path.abspath(os.path.dirname(__file__) + "/..")
ui_path = os.path.join(workspace, "01_systems", "KALMIYA_System", "ui")

sys.path.insert(0, ui_path)
sys.path.insert(0, workspace)

from kalmiya_chat_simple_tkinter import KalmiyaChatSimple

if __name__ == "__main__":
    app = KalmiyaChatSimple()
    app.run()
