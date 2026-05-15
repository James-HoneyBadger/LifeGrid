pub mod ant;
pub mod briansbrain;
pub mod conway;
pub mod generations;
pub mod hexagonal;
pub mod highlife;
pub mod immigration;
pub mod lifelike;
pub mod rainbow;
pub mod wireworld;

pub use ant::LangtonsAnt;
pub use briansbrain::BriansBrain;
pub use conway::ConwayLife;
pub use generations::Generations;
pub use hexagonal::HexagonalLife;
pub use highlife::HighLife;
pub use immigration::ImmigrationGame;
pub use lifelike::LifeLike;
pub use rainbow::RainbowGame;
pub use wireworld::Wireworld;

use crate::core::{BoundaryMode, Grid};

// ---------------------------------------------------------------------------
// Automaton trait
// ---------------------------------------------------------------------------

/// Common interface for all cellular automata.
pub trait Automaton {
    fn name(&self) -> &'static str;
    fn step(&mut self);
    fn reset(&mut self);
    fn get_grid(&self) -> &Grid;
    fn get_grid_mut(&mut self) -> &mut Grid;
    fn handle_click(&mut self, x: usize, y: usize);
    fn load_pattern(&mut self, pattern: &str);
    fn available_patterns(&self) -> &'static [&'static str];
    fn boundary(&self) -> BoundaryMode;
    fn set_boundary(&mut self, mode: BoundaryMode);

    fn width(&self) -> usize {
        self.get_grid().width
    }
    fn height(&self) -> usize {
        self.get_grid().height
    }
}

// ---------------------------------------------------------------------------
// Factory
// ---------------------------------------------------------------------------

/// All supported automaton modes in display order.
pub const ALL_MODES: &[&str] = &[
    "Conway's Game of Life",
    "High Life",
    "Hexagonal Life",
    "Immigration Game",
    "Rainbow Game",
    "Langton's Ant",
    "Wireworld",
    "Brian's Brain",
    "Generations",
    "Custom Rules",
];

/// Build a boxed automaton for the given mode string.
pub fn make_automaton(mode: &str, width: usize, height: usize) -> Box<dyn Automaton> {
    match mode {
        "Conway's Game of Life" => Box::new(ConwayLife::new(width, height)),
        "High Life" => Box::new(HighLife::new(width, height)),
        "Hexagonal Life" => Box::new(HexagonalLife::new(width, height)),
        "Immigration Game" => Box::new(ImmigrationGame::new(width, height)),
        "Rainbow Game" => Box::new(RainbowGame::new(width, height)),
        "Langton's Ant" => Box::new(LangtonsAnt::new(width, height)),
        "Wireworld" => Box::new(Wireworld::new(width, height)),
        "Brian's Brain" => Box::new(BriansBrain::new(width, height)),
        "Generations" => Box::new(Generations::new(width, height)),
        "Custom Rules" => Box::new(LifeLike::new(width, height, vec![3], vec![2, 3])),
        _ => Box::new(ConwayLife::new(width, height)),
    }
}
