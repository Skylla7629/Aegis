use std::io;

use ratatui::{DefaultTerminal, Frame, buffer::Buffer, crossterm::event::{self, Event, KeyCode, KeyEvent, KeyEventKind}, layout::{Constraint, Layout, Rect}, symbols::border, text::{Line, Text}, widgets::{Block, Paragraph, Widget}};


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
        frame.render_widget(self, frame.area());
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

impl Widget for &App {
    fn render(self, area: Rect, buf: &mut Buffer) {
        let title = Line::from(" Aegis - Secure Chatting ");

        let block = Block::bordered()
            .title(title.centered())
            .border_set(border::ROUNDED);

        let text = Text::from(vec![
            Line::from(vec![
                "Text".into(),
            ])
        ]);

        Paragraph::new(text)
            .centered()
            .block(block)
            .render(area,buf);
    }
}