import curses
import time

def main(stdscr):
    # Clear screen
    stdscr.clear()
    
    # turn off cursor blinking
    curses.curs_set(0)

    # Get screen height/width
    height, width = stdscr.getmaxyx()

    # Create a centered text
    text = "Hello from Curses!"
    x = width // 2 - len(text) // 2
    y = height // 2

    # Add text (y, x, string, attributes)
    stdscr.addstr(y, x, text, curses.A_BOLD)

    # Refresh the screen to show changes
    stdscr.refresh()

    # Wait for user input (blocks until keypress)
    stdscr.getch()

# curses.wrapper handles initialization and cleanup safely
curses.wrapper(main)