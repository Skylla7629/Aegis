use crate::tui::app::App;

pub fn start() {
    let mut terminal = ratatui::init();
    let _ = App::new().run(&mut terminal);
    ratatui::restore();
}