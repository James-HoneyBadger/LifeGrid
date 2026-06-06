use rand::Rng;

use crate::core::{BoundaryMode, Grid};

use super::Automaton;

/// Maze - B3/S12345.
pub struct Maze {
    grid: Grid,
    boundary: BoundaryMode,
}

impl Maze {
    pub fn new(width: usize, height: usize) -> Self {
        Self {
            grid: Grid::new(width, height),
            boundary: BoundaryMode::Wrap,
        }
    }
}

impl Automaton for Maze {
    fn name(&self) -> &'static str {
        "Maze"
    }

    fn step(&mut self) {
        let neighbors = self.grid.neighbor_counts(self.boundary, 1);
        let old = self.grid.cells.clone();
        for i in 0..old.len() {
            let alive = old[i] == 1;
            let n = neighbors[i];
            self.grid.cells[i] = if alive {
                u8::from(matches!(n, 1 | 2 | 3 | 4 | 5))
            } else {
                u8::from(n == 3)
            };
        }
    }

    fn reset(&mut self) {
        self.grid.clear();
    }

    fn get_grid(&self) -> &Grid {
        &self.grid
    }

    fn get_grid_mut(&mut self) -> &mut Grid {
        &mut self.grid
    }

    fn handle_click(&mut self, x: usize, y: usize) {
        let v = self.grid.get(y, x);
        self.grid.set(y, x, 1 - v);
    }

    fn load_pattern(&mut self, _pattern: &str) {
        self.grid.clear();
        let w = self.grid.width;
        let h = self.grid.height;
        let cx = (w / 2) as i32;
        let cy = (h / 2) as i32;

        match _pattern {
            "Ladder" => {
                let pts = [
                    (-4, -3), (-4, -2), (-4, -1), (-4, 0), (-4, 1), (-4, 2), (-4, 3),
                    (4, -3), (4, -2), (4, -1), (4, 0), (4, 1), (4, 2), (4, 3),
                    (-3, -2), (-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2), (3, -2),
                    (-3, 0), (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (3, 0),
                    (-3, 2), (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2), (3, 2),
                ];
                for &(dx, dy) in &pts {
                    let x = cx + dx;
                    let y = cy + dy;
                    if x >= 0 && y >= 0 && (x as usize) < w && (y as usize) < h {
                        self.grid.set(y as usize, x as usize, 1);
                    }
                }
            }
            "Core" => {
                let pts = [
                    (-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2),
                    (-2, -1), (2, -1),
                    (-2, 0), (0, 0), (2, 0),
                    (-2, 1), (2, 1),
                    (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2),
                ];
                for &(dx, dy) in &pts {
                    let x = cx + dx;
                    let y = cy + dy;
                    if x >= 0 && y >= 0 && (x as usize) < w && (y as usize) < h {
                        self.grid.set(y as usize, x as usize, 1);
                    }
                }
            }
            "Random Soup" | _ => {
                let mut rng = rand::thread_rng();
                for cell in self.grid.cells.iter_mut() {
                    *cell = u8::from(rng.gen::<f32>() < 0.15);
                }
            }
        }
    }

    fn available_patterns(&self) -> &'static [&'static str] {
        &["Ladder", "Core", "Random Soup"]
    }

    fn boundary(&self) -> BoundaryMode {
        self.boundary
    }

    fn set_boundary(&mut self, mode: BoundaryMode) {
        self.boundary = mode;
    }
}
