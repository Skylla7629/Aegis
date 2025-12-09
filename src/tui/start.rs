use std::io;

use ratatui::{DefaultTerminal, Frame, buffer::Buffer, crossterm::event::{self, Event, KeyCode, KeyEvent, KeyEventKind}, layout::{Constraint, Direction, Layout, Rect}, symbols::border, text::{Line, Text}, widgets::{Block, Borders, Paragraph, Widget}};


pub fn start() {
    let mut terminal = ratatui::init();
    let _ = App::default().run(&mut terminal);
    ratatui::restore();
}

// struct to keep Track of values from the TUI
#[derive(Default)]
struct App {
    // App active
    exit: bool,
    // List of Chatnames
    _chats_names: Vec<String>,
    cols: usize,
    rows: usize,
}
impl App {
    pub fn run(&mut self, terminal: &mut DefaultTerminal) -> color_eyre::Result<()> {
        while !self.exit {
            terminal.draw(|frame| self.draw(frame))?;
            self.handle_events()?;
        }
        Ok(())
    }

    fn draw(&self, frame: &mut Frame) {
        let layout_areas = Self::create_chat_layout(frame.area());

        Self::render_chat_picker_widget(frame, layout_areas[0], self);
        Self::render_messages_widget(frame, layout_areas[1], self);
        Self::render_input_widget(frame, layout_areas[2], self);
    }

    fn render_input_widget(frame: &mut Frame, area: Rect, app_state: &App) {
        let input = Paragraph::new("input")
            .block(Block::default().borders(Borders::LEFT | Borders::RIGHT));
        frame.render_widget(input, area);
    }

    fn render_chat_picker_widget(frame: &mut Frame, area: Rect, app_state: &App) {
        let status = Paragraph::new("Chat Picker")
            .block(Block::default().borders(Borders::LEFT | Borders::RIGHT));
        frame.render_widget(status, area);
    }

    fn render_messages_widget(frame: &mut Frame, area: Rect, app_state: &App) {
        let history_text = &app_state._chats_names; 

        let messages = Paragraph::new("messages")
            .block(Block::default().borders(Borders::ALL).title("Messages"));

        frame.render_widget(messages, area);
    }

    fn create_chat_layout (area: Rect) -> [Rect; 3] {
        let layout = Layout::new(
            Direction::Horizontal,
            [
                Constraint::Percentage(25),
                Constraint::Min(25),
            ])
            .split(area);
        let content_area = layout[1];
        let chat_area = Layout::vertical([
            Constraint::Min(3),
            Constraint::Length(3),
        ])
        .split(content_area);
        [layout[0], chat_area[0], chat_area[1]]
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
            KeyCode::Char('q') => self.exit = true,
            _ => {}
        }
    }
}