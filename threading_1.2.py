#!/usr/bin/env python3
import threading
import time
import curses
import queue

# Shared flag variable for signaling download completion
download_complete = False

# Function to simulate file download
def download_file(progress_queue):
    try:
        for i in range(10):
            message = f"Downloading... {i * 10}%\n"
            progress_queue.put(message)
            time.sleep(1)
        progress_queue.put("Download complete")
    except KeyboardInterrupt:
        # Handle Ctrl+C, and set download_complete flag to True
        global download_complete
        download_complete = True

# Function to display download progress
def display_download_progress(stdscr, progress_queue):
    while not download_complete or not progress_queue.empty():
        try:
            message = progress_queue.get_nowait()
            stdscr.addstr(message)
            stdscr.refresh()
        except curses.error:
            pass

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
    progress_queue = queue.Queue()
    download_thread = threading.Thread(target=download_file, args=(progress_queue,))
    download_thread.start()

    # Start a separate thread to display download progress
    display_thread = threading.Thread(target=display_download_progress, args=(stdscr, progress_queue))
    display_thread.start()

    # Start reading keyboard input in a separate thread
    input_thread = threading.Thread(target=read_keyboard_input, args=(stdscr,))
    input_thread.start()

    # Wait for the download to complete
    download_thread.join()

    # Wait for the input thread to finish
    input_thread.join()

    # Wait for the display thread to finish
    display_thread.join()

except KeyboardInterrupt:
    pass  # Handle Ctrl+C gracefully

finally:
    # Cleanup curses
    curses.endwin()
    import os
    os.system("clear")  # Clears the terminal (Unix-like systems)
    # On Windows, you can use "cls" instead of "clear"
