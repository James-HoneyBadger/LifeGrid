use rand::Rng;

use crate::core::{BoundaryMode, Grid};

use super::Automaton;

/// Seeds - B2/S.
pub struct Seeds {
    grid: Grid,
    boundary: BoundaryMode,
}

impl Seeds {
    pub fn new(width: usize, height: usize) -> Self {
        Self {
            grid: Grid::new(width, height),
            boundary: BoundaryMode::Wrap,
        }
    }
}

impl Automaton for Seeds {
    fn name(&self) -> &'static str {
        "Seeds"
    }

    fn step(&mut self) {
        let neighbors = self.grid.neighbor_counts(self.boundary, 1);
        let old = self.grid.cells.clone();
        for i in 0..old.len() {
            let alive = old[i] == 1;
            let n = neighbors[i];
            self.grid.cells[i] = if alive {
                0
            } else {
                u8::from(n == 2)
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
            "Twin Pairs" => {
                let pts = [
                    (-4, -1), (-3, -1),
                    (3, 1), (4, 1),
                    (-1, 3), (0, 3),
                ];
                for &(dx, dy) in &pts {
                    let x = cx + dx;
                    let y = cy + dy;
                    if x >= 0 && y >= 0 && (x as usize) < w && (y as usize) < h {
                        self.grid.set(y as usize, x as usize, 1);
                    }
                }
            }
            "Seed Ring" => {
                let pts = [
                    (-3, -3), (0, -3), (3, -3),
                    (-3, 0), (3, 0),
                    (-3, 3), (0, 3), (3, 3),
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
        &["Twin Pairs", "Seed Ring", "Random Soup"]
    }

    fn boundary(&self) -> BoundaryMode {
        self.boundary
    }

    fn set_boundary(&mut self, mode: BoundaryMode) {
        self.boundary = mode;
    }
}
