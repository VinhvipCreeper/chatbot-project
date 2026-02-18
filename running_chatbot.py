"""
running_chatbot.py
------------------
Run this file to open a new terminal window with the chatbot launched inside it.

    python running_chatbot.py
"""

import subprocess
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

subprocess.Popen(
    ["cmd", "/k", "python chatbot.py"],
    cwd=script_dir,
    creationflags=subprocess.CREATE_NEW_CONSOLE,
)
