use std::io;

use crossterm::terminal::LeaveAlternateScreen;
use ratatui::{Terminal, backend, crossterm::{execute, terminal::{EnterAlternateScreen, enable_raw_mode}}, prelude::CrosstermBackend};


pub fn main() {
    enable_raw_mode();
    execute!(io::stdout(), EnterAlternateScreen);
    let backend = CrosstermBackend::new(io::stdout());
    let mut terminal = Terminal::new(backend);
    print!("print");
}