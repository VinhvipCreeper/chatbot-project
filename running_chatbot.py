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
    ["cmd", "/k", f'cd /d "{script_dir}" && python chatbot.py'],
    creationflags=subprocess.CREATE_NEW_CONSOLE,
)
