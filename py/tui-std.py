import sys
import time
import os

# --- ANSI Constants ---
ESC = "\033"
CLEAR = f"{ESC}[2J"
# Move cursor to top-left
HOME = f"{ESC}[H" 
# Red text
RED = f"{ESC}[31m" 
# Reset colors
RESET = f"{ESC}[0m" 
# Hide Cursor
HIDE_CURSOR = f"{ESC}[?25l"
# Show Cursor
SHOW_CURSOR = f"{ESC}[?25h"
# Inverse
SELECTION_STYLE = f"{ESC}[7m"

class KeyboardListener:
    """
    A cross-platform keyboard listener using only Python standard libraries.
    Works on Windows, Linux, and macOS.
    """
    def __init__(self):
        self.os_type = sys.platform
        
        # Windows uses msvcrt
        if self.os_type == 'win32':
            import msvcrt
            self.msvcrt = msvcrt
        
        # Linux/macOS uses termios/tty
        else:
            import tty
            import termios
            self.tty = tty
            self.termios = termios

    def get_key(self):
        """
        Reads a single character from standard input without requiring the user 
        to press Enter. This blocks execution until a key is pressed.
        """
        if self.os_type == 'win32':
            # Windows implementation
            # getch() returns bytes, so we decode it
            # msvcrt.getch() reads a keypress and returns the resulting character.
            key = self.msvcrt.getch()
            try:
                return key.decode('utf-8')
            except UnicodeDecodeError:
                # Handle special keys (arrows, function keys) which return multi-byte codes
                return 'special_key'

        else:
            # Unix/Linux/macOS implementation
            # We must switch the terminal to 'raw' mode to read 1 byte at a time
            # instead of waiting for a newline (canonical mode).
            fd = sys.stdin.fileno()
            old_settings = self.termios.tcgetattr(fd)
            try:
                self.tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                # Always restore terminal settings to normal, otherwise the
                # terminal will remain in a weird state after exit.
                self.termios.tcsetattr(fd, self.termios.TCSADRAIN, old_settings)
            return ch


class ScreenCursor:
    def __init__(self):
        self.pos_y = 1
        self.pos_x = 1

    def write(self, text):
        """Writes text at current cursor position."""
        sys.stdout.write(text)
        sys.stdout.flush()
        # Update cursor position
        lines = text.split('\n')
        if len(lines) == 1:
            self.pos_x += len(lines[0])
        else:
            self.pos_y += len(lines) - 1
            self.pos_x = len(lines[-1]) + 1

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

def draw_menu(cursor:ScreenCursor):
    cursor.write(HIDE_CURSOR)
    cursor.write(CLEAR)
    cursor.move_to(1, 1)
    cursor.write("Simple TUI Example\n")
    cursor.write("-------------------\n")
    global op1Pos, op2Pos
    op1Pos = (cursor.pos_y, cursor.pos_x)
    cursor.write("1. Option\n\n")
    op2Pos = (cursor.pos_y, cursor.pos_x)
    cursor.write("2. Option\n\n")
    cursor.write("Press 'q' to quit.\n")

def main():
    listener = KeyboardListener()
    cursor = ScreenCursor()
    try:
        # 1. Setup screen
        os.system('cls' if os.name == 'nt' else 'clear') # Basic flush
        draw_menu(cursor)
        
        while True:
            # Flush buffer to ensure it displays immediately
            key = listener.get_key()
            
            match key:
                case 'q':
                    break
                case '1':
                    draw_menu(cursor)  # Redraw menu to clear previous selection
                    cursor.move_to(*op1Pos)
                    cursor.write(SELECTION_STYLE + "1. Option" + RESET)
                case '2':
                    draw_menu(cursor)  # Redraw menu to clear previous selection
                    cursor.move_to(*op2Pos)
                    cursor.write(SELECTION_STYLE + "2. Option" + RESET)
                case _:
                    cursor.move_to(12, 5)
                    cursor.write(" " * 30)  # Clear line
                    cursor.move_to(12, 5)
                    cursor.write("Invalid option. Press '1', '2', or 'q' to quit.")

            sys.stdout.flush()
                            
            time.sleep(0.1)

    except KeyboardInterrupt:
        # Handle exit gracefully
        pass
    finally:
        cursor.quit()

if __name__ == "__main__":
    main()
    
# EOF