use crate::tui::app::App;

pub fn start() {
    let mut terminal = ratatui::init();
    let _ = App::default().run(&mut terminal);
    ratatui::restore();
}