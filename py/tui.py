##
import threading
import sys
import os
import signal

# --- ANSI Constants ---
ESC = "\033"
CLEAR = f"{ESC}[2J"
HOME = f"{ESC}[H" 
RED = f"{ESC}[31m" 
RESET = f"{ESC}[0m" 
HIDE_CURSOR = f"{ESC}[?25l"
SHOW_CURSOR = f"{ESC}[?25h"
SELECTION_STYLE = f"{ESC}[7m"

class KeyboardListener:
    """
    A cross-platform keyboard listener using only Python standard libraries.
    Works on Windows, Linux, and macOS.
    """
    def __init__(self):
        # Linux/macOS uses termios/tty
        import tty
        import termios
        import select
        self.tty = tty
        self.termios = termios
        self.select = select

    def get_key(self):
        """
        Reads a single character from standard input without requiring the user 
        to press Enter. This blocks execution until a key is pressed.
        """
        # Unix/Linux/macOS implementation
        # We must switch the terminal to 'raw' mode to read 1 byte at a time
        # instead of waiting for a newline (canonical mode).
        fd = sys.stdin.fileno()
        old_settings = self.termios.tcgetattr(fd)
        try:
            self.tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            
            # Handle Escape Sequences (Arrow keys start with ESC \x1b)
            if ch == '\x1b':
                # Check if there are more characters waiting (non-blocking peek)
                # If nothing follows immediately, it was just the ESC key.
                # Setting timeout to 0 makes it instant.
                if self.select.select([sys.stdin], [], [], 0)[0]:
                    # Read the next two characters (expected '[A', '[B', etc.)
                    seq = sys.stdin.read(2)
                    
                    if seq == '[A': return 'KEY_UP'
                    if seq == '[B': return 'KEY_DOWN'
                    if seq == '[C': return 'KEY_RIGHT'
                    if seq == '[D': return 'KEY_LEFT'
                    
            return ch

        finally:
            # Always restore terminal settings to normal, otherwise the
            # terminal will remain in a weird state after exit.
            self.termios.tcsetattr(fd, self.termios.TCSADRAIN, old_settings)
                                

class ScreenCursor:
    def __init__(self):
        self.pos_y = 1
        self.pos_x = 1

    def write(self, text):
        """Writes text at current cursor position."""
        
        init_pos_x = self.pos_x
        init_pos_y = self.pos_y
        for _, line in enumerate(text.split('\n')):
            sys.stdout.write(line)
            self.pos_x += len(line)
            self.move_to(self.pos_y + _, init_pos_x)
        sys.stdout.flush()

    def move_to(self, y, x):
        """Moves cursor to (y, x) position."""
        sys.stdout.write(f"{ESC}[{y};{x}H")
        self.pos_y = y
        self.pos_x = x

    def lines_down(self, n=1):
        """Moves cursor down by n lines."""
        self.pos_y += n
        sys.stdout.write(f"{ESC}[{n}B")

    def lines_up(self, n=1):
        """Moves cursor up by n lines."""
        self.pos_y -= n
        sys.stdout.write(f"{ESC}[{n}A")
                         
    def quit(self):
        """Restores cursor visibility and exits."""
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.write(RESET)
        sys.stdout.write(CLEAR)
        sys.stdout.write(HOME)
        sys.stdout.flush()
        print("Goodbye!")



class TUI(threading.Thread):
    def __init__(self) -> None:
        super().__init__()
        self.kbListener = KeyboardListener()
        self.cursor = ScreenCursor()
        if hasattr(signal, 'SIGWINCH'):
            signal.signal(signal.SIGWINCH, self.on_resize)
        signal.signal(signal.SIGINT, self.on_exit)

    def get_size(self):
        """Returns terminal size as (rows, cols)."""
        return os.get_terminal_size().lines, os.get_terminal_size().columns

    def on_resize(self, signum, frame):
        # Handle terminal resize events if needed
        self.paint_screen()

    def on_exit(self, signum, frame):
        self.cursor.quit()
        sys.exit(0)

    def paint_screen(self):
        self.cursor.write(CLEAR)
        self.cursor.move_to(1, 1)
        rows, cols = self.get_size()
        
        # draw border
        self.cursor.write(f"{RED}+{'-' * (cols//3)}+{'-' * (cols -3- cols//3)}+{RESET}\n")
        for _ in range(rows - 8):
            self.cursor.write(f"{RED}|{RESET}{' ' * (cols//3)}{RED}|{RESET}{' ' * (cols -3- cols//3)}{RED}|{RESET}\n")
        self.cursor.write(f"{RED}+{' ' * (cols//3)}+{'-' * (cols -3- cols//3)}+{RESET}\n")
        for _ in range(5):
            self.cursor.write(f"{RED}|{RESET}{' ' * (cols//3)}{RED}|{RESET}{' ' * (cols -3- cols//3)}{RED}|{RESET}\n")
        self.cursor.write(f"{RED}+{'-' * (cols//3)}+{'-' * (cols -3- cols//3)}+{RESET}\n")


    def insert_mode(self):
        self.cursor.move_to(self.get_size()[0]-4, 5)
        self.cursor.write("INSERT MODE: Type your message (Press ESC to exit)\n")
        buffer = ""
        while True:
            key = self.kbListener.get_key()
            if key == '\x1b':  # ESC key
                break
            elif key == '\x7f':  # Backspace
                if len(buffer) > 0:
                    buffer = buffer[:-1]
                    self.cursor.move_to(self.get_size()[0]-3, 5)
                    self.cursor.write(' ' * (len(buffer) + 1))
                    self.cursor.move_to(self.get_size()[0]-3, 5)
                    self.cursor.write(buffer)
            else:
                buffer += key
                self.cursor.move_to(self.get_size()[0]-3, 5)
                self.cursor.write(buffer)
        self.cursor.move_to(self.get_size()[0]-4, 5)
        self.cursor.write(' ' * 50)
        self.cursor.move_to(self.get_size()[0]-3, 5)
        self.cursor.write(' ' * 50)


    def run(self) -> None:
        self.cursor.write(HIDE_CURSOR)
        self.cursor.write(CLEAR)
        self.cursor.move_to(1, 1)
        self.paint_screen()
        self.cursor.move_to(3, 5)
        self.cursor.write("TUI Started. Press 'q' to quit.\n")
        self.cursor.write(f"{RED}Terminal Size: {self.get_size()[0]} rows x {self.get_size()[1]} cols{RESET}\n")
        
        self.cursor.write(SHOW_CURSOR)

        while True:
            key = self.kbListener.get_key()
            if key == 'q':
                break
            elif key == 'i':
                self.insert_mode()
            self.cursor.move_to(10, 5)
            #self.cursor.write(f"You pressed: {key}\n")
        self.cursor.quit()



# EOF