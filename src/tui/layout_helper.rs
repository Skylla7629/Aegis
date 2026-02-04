use ratatui::layout::{Constraint, Direction, Layout, Rect};
use crate::tui::app::App;

impl App {
    pub fn create_chat_layout (area: Rect) -> [Rect; 3] {
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
}