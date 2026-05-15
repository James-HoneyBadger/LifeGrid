use std::collections::VecDeque;

/// Circular undo/redo stack for grid snapshots.
pub struct UndoManager {
    undo_stack: VecDeque<Vec<u8>>,
    redo_stack: VecDeque<Vec<u8>>,
    max_history: usize,
}

impl UndoManager {
    pub fn new(max_history: usize) -> Self {
        Self {
            undo_stack: VecDeque::new(),
            redo_stack: VecDeque::new(),
            max_history,
        }
    }

    pub fn push(&mut self, state: Vec<u8>) {
        if self.undo_stack.len() >= self.max_history {
            self.undo_stack.pop_front();
        }
        self.undo_stack.push_back(state);
        self.redo_stack.clear();
    }

    /// Returns the previous state (caller must save current state first).
    pub fn undo(&mut self, current: Vec<u8>) -> Option<Vec<u8>> {
        let prev = self.undo_stack.pop_back()?;
        if self.redo_stack.len() >= self.max_history {
            self.redo_stack.pop_front();
        }
        self.redo_stack.push_back(current);
        Some(prev)
    }

    pub fn redo(&mut self, current: Vec<u8>) -> Option<Vec<u8>> {
        let next = self.redo_stack.pop_back()?;
        if self.undo_stack.len() >= self.max_history {
            self.undo_stack.pop_front();
        }
        self.undo_stack.push_back(current);
        Some(next)
    }

    pub fn clear(&mut self) {
        self.undo_stack.clear();
        self.redo_stack.clear();
    }

    pub fn can_undo(&self) -> bool {
        !self.undo_stack.is_empty()
    }

    pub fn can_redo(&self) -> bool {
        !self.redo_stack.is_empty()
    }
}

impl Default for UndoManager {
    fn default() -> Self {
        Self::new(100)
    }
}
