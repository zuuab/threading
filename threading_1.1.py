#!/usr/bin/env python3
import threading
import time
import curses

# Shared flag variable for signaling download completion
download_complete = False

# Function to simulate file download
def download_file():
    try:
        for i in range(10):
            print(f"Downloading... {i * 10}%")
            time.sleep(1)
    except KeyboardInterrupt:
        # Handle Ctrl+C, and set download_complete flag to True
        global download_complete
        download_complete = True

# Function to read keyboard input
def read_keyboard_input(stdscr):
    stdscr.nodelay(1)  # Enable non-blocking input
    while not download_complete:
        key = stdscr.getch()
        if key != -1:
            # Handle the key input here
            print(f"Key pressed: {chr(key)}")

# Initialize curses and create a window
stdscr = curses.initscr()

try:
    # Start the file download in a separate thread
    download_thread = threading.Thread(target=download_file)
    download_thread.start()

    # Start reading keyboard input in a separate thread
    input_thread = threading.Thread(target=read_keyboard_input, args=(stdscr,))
    input_thread.start()

    # Wait for the download to complete
    download_thread.join()

    # Wait for the input thread to finish
    input_thread.join()

except KeyboardInterrupt:
    pass  # Handle Ctrl+C gracefully

finally:
    # Cleanup curses
    curses.endwin()
