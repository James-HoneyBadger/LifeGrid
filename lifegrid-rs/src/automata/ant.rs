use crate::core::{BoundaryMode, Grid};

use super::Automaton;

/// Langton's Ant – single ant on a binary grid.
pub struct LangtonsAnt {
    /// True cell states (0/1).
    base: Grid,
    /// Display copy with ant position marked as state 2.
    display: Grid,
    pub ant_x: usize,
    pub ant_y: usize,
    /// 0 = North, 1 = East, 2 = South, 3 = West
    pub ant_dir: u8,
    boundary: BoundaryMode,
}

impl LangtonsAnt {
    pub fn new(width: usize, height: usize) -> Self {
        let mut s = Self {
            base: Grid::new(width, height),
            display: Grid::new(width, height),
            ant_x: width / 2,
            ant_y: height / 2,
            ant_dir: 0,
            boundary: BoundaryMode::Wrap,
        };
        s.sync_display();
        s
    }

    fn sync_display(&mut self) {
        self.display.cells.clone_from(&self.base.cells);
        self.display.set(self.ant_y, self.ant_x, 2);
    }
}

impl Automaton for LangtonsAnt {
    fn name(&self) -> &'static str {
        "Langton's Ant"
    }

    fn step(&mut self) {
        let current = self.base.get(self.ant_y, self.ant_x);
        self.base.set(self.ant_y, self.ant_x, 1 - current);

        if current == 0 {
            self.ant_dir = (self.ant_dir + 1) % 4;
        } else {
            self.ant_dir = (self.ant_dir + 3) % 4;
        }

        let h = self.base.height;
        let w = self.base.width;
        let (next_y, next_x) = match self.ant_dir {
            0 => (self.ant_y as i32 - 1, self.ant_x as i32),
            1 => (self.ant_y as i32, self.ant_x as i32 + 1),
            2 => (self.ant_y as i32 + 1, self.ant_x as i32),
            _ => (self.ant_y as i32, self.ant_x as i32 - 1),
        };

        if let Some((ry, rx)) = self.boundary.resolve(next_y, next_x, h, w) {
            self.ant_y = ry;
            self.ant_x = rx;
        }

        self.sync_display();
    }

    fn reset(&mut self) {
        self.base.clear();
        self.ant_x = self.base.width / 2;
        self.ant_y = self.base.height / 2;
        self.ant_dir = 0;
        self.sync_display();
    }

    fn get_grid(&self) -> &Grid {
        &self.display
    }

    fn get_grid_mut(&mut self) -> &mut Grid {
        &mut self.base
    }

    fn handle_click(&mut self, x: usize, y: usize) {
        self.ant_x = x;
        self.ant_y = y;
        self.sync_display();
    }

    fn load_pattern(&mut self, _pattern: &str) {
        self.reset();
    }

    fn available_patterns(&self) -> &'static [&'static str] {
        &["Empty"]
    }

    fn boundary(&self) -> BoundaryMode {
        self.boundary
    }

    fn set_boundary(&mut self, mode: BoundaryMode) {
        self.boundary = mode;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn wraps_at_top_edge() {
        let mut ant = LangtonsAnt::new(5, 5);
        ant.set_boundary(BoundaryMode::Wrap);
        ant.ant_x = 2;
        ant.ant_y = 0;
        ant.ant_dir = 3; // facing West; on white cell it turns North and moves.
        ant.base.clear();
        ant.sync_display();

        ant.step();

        assert_eq!((ant.ant_x, ant.ant_y), (2, 4));
    }

    #[test]
    fn fixed_boundary_blocks_out_of_bounds_step() {
        let mut ant = LangtonsAnt::new(5, 5);
        ant.set_boundary(BoundaryMode::Fixed);
        ant.ant_x = 2;
        ant.ant_y = 0;
        ant.ant_dir = 3; // facing West; on white cell it turns North and would step out.
        ant.base.clear();
        ant.sync_display();

        ant.step();

        assert_eq!((ant.ant_x, ant.ant_y), (2, 0));
    }

    #[test]
    fn reflect_boundary_mirrors_at_top_edge() {
        let mut ant = LangtonsAnt::new(5, 5);
        ant.set_boundary(BoundaryMode::Reflect);
        ant.ant_x = 2;
        ant.ant_y = 0;
        ant.ant_dir = 3; // facing West; on white cell it turns North and reflects.
        ant.base.clear();
        ant.sync_display();

        ant.step();

        assert_eq!((ant.ant_x, ant.ant_y), (2, 0));
    }
}
