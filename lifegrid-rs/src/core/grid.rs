use super::BoundaryMode;

/// A flat, heap-allocated 2-D grid of `u8` cells.
///
/// Indices are row-major: `cells[y * width + x]`.
#[derive(Clone)]
pub struct Grid {
    pub cells: Vec<u8>,
    pub width: usize,
    pub height: usize,
}

impl Grid {
    pub fn new(width: usize, height: usize) -> Self {
        Self {
            cells: vec![0; width * height],
            width,
            height,
        }
    }

    #[inline]
    pub fn get(&self, y: usize, x: usize) -> u8 {
        self.cells[y * self.width + x]
    }

    #[inline]
    pub fn set(&mut self, y: usize, x: usize, val: u8) {
        self.cells[y * self.width + x] = val;
    }

    pub fn clear(&mut self) {
        self.cells.fill(0);
    }

    /// Number of non-zero cells.
    pub fn population(&self) -> usize {
        self.cells.iter().filter(|&&c| c > 0).count()
    }

    // -----------------------------------------------------------------------
    // Neighbour helpers
    // -----------------------------------------------------------------------

    /// Compute the count of 8-neighbours whose value equals `check_val` for
    /// every cell, returning a flat `Vec<u8>` with the same layout.
    pub fn neighbor_counts(&self, boundary: BoundaryMode, check_val: u8) -> Vec<u8> {
        let h = self.height;
        let w = self.width;
        let mut counts = vec![0u8; h * w];
        for y in 0..h {
            for x in 0..w {
                let mut c = 0u8;
                for dy in -1i32..=1 {
                    for dx in -1i32..=1 {
                        if dy == 0 && dx == 0 {
                            continue;
                        }
                        if let Some((ny, nx)) =
                            boundary.resolve(y as i32 + dy, x as i32 + dx, h, w)
                        {
                            if self.get(ny, nx) == check_val {
                                c += 1;
                            }
                        }
                    }
                }
                counts[y * w + x] = c;
            }
        }
        counts
    }

    /// Like [`neighbor_counts`] but counts any cell with `value > 0`.
    pub fn neighbor_counts_alive(&self, boundary: BoundaryMode) -> Vec<u8> {
        let h = self.height;
        let w = self.width;
        let mut counts = vec![0u8; h * w];
        for y in 0..h {
            for x in 0..w {
                let mut c = 0u8;
                for dy in -1i32..=1 {
                    for dx in -1i32..=1 {
                        if dy == 0 && dx == 0 {
                            continue;
                        }
                        if let Some((ny, nx)) =
                            boundary.resolve(y as i32 + dy, x as i32 + dx, h, w)
                        {
                            if self.get(ny, nx) > 0 {
                                c += 1;
                            }
                        }
                    }
                }
                counts[y * w + x] = c;
            }
        }
        counts
    }

    /// Returns `(alive_count, color_sum)` neighbour arrays, used by
    /// multi-state automata like Immigration and Rainbow.
    pub fn neighbor_stats_alive(&self, boundary: BoundaryMode) -> (Vec<u8>, Vec<u32>) {
        let h = self.height;
        let w = self.width;
        let mut counts = vec![0u8; h * w];
        let mut sums = vec![0u32; h * w];
        for y in 0..h {
            for x in 0..w {
                let mut c = 0u8;
                let mut s = 0u32;
                for dy in -1i32..=1 {
                    for dx in -1i32..=1 {
                        if dy == 0 && dx == 0 {
                            continue;
                        }
                        if let Some((ny, nx)) =
                            boundary.resolve(y as i32 + dy, x as i32 + dx, h, w)
                        {
                            let v = self.get(ny, nx);
                            if v > 0 {
                                c += 1;
                                s += v as u32;
                            }
                        }
                    }
                }
                let idx = y * w + x;
                counts[idx] = c;
                sums[idx] = s;
            }
        }
        (counts, sums)
    }
}
