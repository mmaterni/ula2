#!/usr/bin/env python3
# coding: utf-8
#!/usr/bin/env python3
# coding: utf-8

import sys
import tkinter as tk
import subprocess
import signal
import os
from pathlib import Path

server_process = None

def start_server():
    global server_process
    script_dir = Path("/u/ulax/ula2")
    os.chdir(script_dir)
    command = ["python", "/u/ulax/ula2/ulaserver.py"]
    server_process = subprocess.Popen(command)

def stop_server():
    server_process.send_signal(signal.SIGINT)
    server_process.wait()
    sys.exit()


def main():
    root = tk.Tk()
    root.configure(bg="black")
    root.title("Server Control")
    screen_width = root.winfo_screenwidth()
    window_width = 200
    window_height = 160
    window_x = screen_width - window_width - 100
    window_y = 100
    root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")
    root.protocol("WM_DELETE_WINDOW", stop_server)

    start_server()

    stop_button = tk.Button(root,
                            text="Stop Server",
                            command=stop_server,
                            font=("Arial", 16, "bold"),
                            fg="white",
                            bg="red")
    stop_button.pack(pady=50)
    root.mainloop()


if __name__ == "__main__":
    main()
