use ratatui::{Frame, layout::Rect, symbols::{self, border}, text::{Line, Span}, widgets::{Block, Borders, List, ListItem, Paragraph}};

use crate::tui::app::App;
impl App {
    pub fn render_input_widget(&self, frame: &mut Frame, area: Rect) {
        let border_set = border::Set {
            top_left: symbols::line::NORMAL.vertical_right,
            bottom_left: symbols::line::NORMAL.horizontal_up,
            top_right: symbols::line::NORMAL.vertical_left,
            ..border::PLAIN
        };
        
        let input = Paragraph::new(self.input.to_string())
            .block(Block::default()
            .borders(Borders::ALL)
            .border_set(border_set)
            .title("Input"));
        frame.render_widget(input, area);
    }

    pub fn render_chat_picker_widget(frame: &mut Frame, area: Rect) {
        let chat_picker = Paragraph::new("")
            .block(Block::default()
            .borders(Borders::TOP | Borders::LEFT | Borders::BOTTOM)
            .title("Chat Picker"));
        frame.render_widget(chat_picker, area);
    }

    pub fn render_messages_widget(&self, frame: &mut Frame, area: Rect) {
        let border_set = border::Set {
            top_left: symbols::line::NORMAL.horizontal_down,
            ..border::PLAIN
        };

        let messages: Vec<ListItem> = self
            .message_history
            .iter()
            .enumerate()
            .map(|(i, m)| {
                let content = Line::from(Span::raw(format!("{i}: {m}")));
                ListItem::new(content)
            })
            .collect();
            
        let messages = List::new(messages)
            .block(Block::default().borders(Borders::LEFT | Borders::RIGHT | Borders::TOP)
            .border_set(border_set)
            .title("Messages"));

        frame.render_widget(messages, area);
    }
}