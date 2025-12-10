use std::io;

use ratatui::{DefaultTerminal, Frame, crossterm::event::{self, Event, KeyCode, KeyEvent, KeyEventKind}, layout::{Constraint, Direction, Layout, Rect}, symbols::{self, border}, widgets::{Block, Borders, Paragraph}};

// struct to keep Track of values from the TUI
#[derive(Default)]
pub struct App {
    // App active
    exit: bool,
    // List of Chatnames
    _chats_names: Vec<String>,
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

        Self::render_chat_picker_widget(frame, layout_areas[0]);
        Self::render_messages_widget(frame, layout_areas[1]);
        Self::render_input_widget(frame, layout_areas[2]);
    }

    fn render_input_widget(frame: &mut Frame, area: Rect) {
        let border_set = border::Set {
            top_left: symbols::line::NORMAL.vertical_right,
            bottom_left: symbols::line::NORMAL.horizontal_up,
            ..border::PLAIN
        };

        let input = Paragraph::new("input")
            .block(Block::default()
            .borders(Borders::ALL)
            .border_set(border_set)
            .title("Input"));
        frame.render_widget(input, area);
    }

    fn render_chat_picker_widget(frame: &mut Frame, area: Rect) {
        let chat_picker = Paragraph::new("Chat Picker")
            .block(Block::default()
            .borders(Borders::TOP | Borders::LEFT | Borders::BOTTOM)
            .title("Chat Picker"));
        frame.render_widget(chat_picker, area);
    }

    fn render_messages_widget(frame: &mut Frame, area: Rect) {
        let border_set = border::Set {
            top_left: symbols::line::NORMAL.horizontal_down,
            ..border::PLAIN
        };

        let messages = Paragraph::new("messages")
            .block(Block::default().borders(Borders::LEFT | Borders::RIGHT | Borders::TOP)
            .border_set(border_set)
            .title("Messages"));

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