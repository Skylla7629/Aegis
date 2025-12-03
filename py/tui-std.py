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

def move_cursor(y, x):
    """Returns ANSI code to move cursor to row y, col x."""
    return f"{ESC}[{y};{x}H"

def draw_box(h, w, y, x):
    """Draws a box using basic ASCII characters."""
    # Draw top border
    sys.stdout.write(move_cursor(y, x))
    sys.stdout.write("+" + "-" * (w - 2) + "+")
    
    # Draw sides
    for i in range(1, h - 1):
        sys.stdout.write(move_cursor(y + i, x))
        sys.stdout.write("|" + " " * (w - 2) + "|")
        
    # Draw bottom
    sys.stdout.write(move_cursor(y + h - 1, x))
    sys.stdout.write("+" + "-" * (w - 2) + "+")

def main():
    try:
        # 1. Setup screen
        os.system('cls' if os.name == 'nt' else 'clear') # Basic flush
        sys.stdout.write(HIDE_CURSOR)
        
        # 2. Draw static UI
        draw_box(10, 40, 5, 5)
        
        sys.stdout.write(move_cursor(6, 7))
        sys.stdout.write(f"{RED}Built-in TUI Demo{RESET}")
        
        sys.stdout.write(move_cursor(8, 7))
        sys.stdout.write("Press Ctrl+C to exit...")
        
        # 3. Simple Animation Loop
        cols = 7
        direction = 1
        while True:
            # Clear the specific line (simple way: overwrite with spaces)
            sys.stdout.write(move_cursor(10, 7))
            sys.stdout.write(" " * 30) 
            
            # Draw the bouncer
            sys.stdout.write(move_cursor(10, cols))
            sys.stdout.write("O")
            
            # Flush buffer to ensure it displays immediately
            sys.stdout.flush()
            
            # Logic
            cols += direction
            if cols > 30 or cols < 7:
                direction *= -1
                
            time.sleep(0.1)

    except KeyboardInterrupt:
        # Handle exit gracefully
        pass
    finally:
        # 4. Cleanup (Crucial!)
        # If you don't do this, the user's terminal might stay hidden/messy
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.write(RESET)
        sys.stdout.write(CLEAR)
        sys.stdout.write(HOME)
        print("Goodbye!")

if __name__ == "__main__":
    main()
    
# EOF