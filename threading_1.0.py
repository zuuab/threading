#!/usr/bin/env python3
import threading
import time
import curses

# Function to simulate file download
def download_file():
    for i in range(10):
        print(f"Downloading... {i * 10}%\n")
        time.sleep(1)

# Function to read keyboard input
def read_keyboard_input(stdscr):
    stdscr.nodelay(1)  # Enable non-blocking input
    while True:
        key = stdscr.getch()
        if key != -1:
            # Handle the key input here
            print(f"Key pressed: {chr(key)}")

# Initialize curses and create a window
stdscr = curses.initscr()

# Start the file download in a separate thread
download_thread = threading.Thread(target=download_file)
download_thread.start()

# Start reading keyboard input in a separate thread
input_thread = threading.Thread(target=read_keyboard_input, args=(stdscr,))
input_thread.start()

# Wait for the download to complete
download_thread.join()

# Cleanup curses
curses.endwin()

# Wait for the input thread to finish
input_thread.join()