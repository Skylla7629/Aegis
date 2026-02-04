use std::io;

use ratatui::{DefaultTerminal, Frame, crossterm::event::{self, Event, KeyCode, KeyEvent, KeyEventKind}};

// struct to keep Track of values from the TUI
#[derive(Default)]
pub struct App {
    // App active
    exit: bool,
    // history of send messages
    pub message_history: Vec<String>,

    // input for the terminal
    pub input: String,
    // position of the cursor in editor
    pub character_index_cursor: usize,

}

impl App {
    pub fn new() -> App {
        App {
            exit: false,
            message_history: vec![],
            input: String::new(),
            character_index_cursor: 0,
        }
    }

    pub fn run(&mut self, terminal: &mut DefaultTerminal) -> color_eyre::Result<()> {
        while !self.exit {
            terminal.draw(|frame| self.draw(frame))?;
            self.handle_events()?;
        }
        Ok(())
    }

    fn draw(&self, frame: &mut Frame) {
        let layout_areas = Self::create_chat_layout(frame.area());

        Self::render_chat_picker_widget(frame, layout_areas[0]);
        Self::render_messages_widget(self, frame, layout_areas[1]);
        Self::render_input_widget(self, frame, layout_areas[2]);
    }

    fn handle_events(&mut self) -> io::Result<()> {
        match event::read()? {
            Event::Key(key_event) if key_event.kind == KeyEventKind::Press => {
                self.handle_key_event(key_event)
            }
            _ => {}
        };
        Ok(())
    }

    fn handle_key_event(&mut self, key_event: KeyEvent) {
        match key_event.code {
            KeyCode::Esc => self.exit = true,
            KeyCode::Enter => self.submit_message(),
            KeyCode::Char(to_insert) => self.enter_char(to_insert),
            KeyCode::Backspace => self.delete_char(),
            KeyCode::Left => self.move_cursor_left(),
            KeyCode::Right => self.move_cursor_right(),
            _ => {}
        }
    }
}