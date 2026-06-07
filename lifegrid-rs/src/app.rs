use std::time::{Duration, Instant};

use egui::{Color32, CornerRadius, Rect, Sense, Vec2};
use rand::Rng;

use crate::automata::{self, Automaton, LifeLike};
use crate::core::{AppConfig, BoundaryMode, UndoManager};
use crate::export;

// ---------------------------------------------------------------------------
// Colour helpers
// ---------------------------------------------------------------------------

fn cell_color(state: u8, dark: bool) -> Color32 {
    if dark {
        match state {
            0 => Color32::from_rgb(14, 14, 22),
            1 => Color32::from_rgb(220, 220, 255),
            2 => Color32::from_rgb(255, 80, 80),
            3 => Color32::from_rgb(255, 160, 0),
            4 => Color32::from_rgb(240, 240, 0),
            5 => Color32::from_rgb(0, 220, 100),
            6 => Color32::from_rgb(60, 140, 255),
            7 => Color32::from_rgb(200, 80, 255),
            8 => Color32::from_rgb(140, 140, 160),
            _ => Color32::from_rgb(100, 100, 120),
        }
    } else {
        match state {
            0 => Color32::WHITE,
            1 => Color32::BLACK,
            2 => Color32::from_rgb(200, 40, 40),
            3 => Color32::from_rgb(210, 110, 0),
            4 => Color32::from_rgb(180, 180, 0),
            5 => Color32::from_rgb(0, 150, 60),
            6 => Color32::from_rgb(0, 60, 200),
            7 => Color32::from_rgb(120, 0, 200),
            8 => Color32::from_rgb(80, 80, 80),
            _ => Color32::from_rgb(120, 120, 120),
        }
    }
}

fn aging_color(base: Color32, age: u32) -> Color32 {
    let t = (age as f32 / 200.0).min(1.0);
    let warm = Color32::from_rgb(255, 180, 40);
    let r = (base.r() as f32 * (1.0 - t) + warm.r() as f32 * t) as u8;
    let g = (base.g() as f32 * (1.0 - t) + warm.g() as f32 * t) as u8;
    let b = (base.b() as f32 * (1.0 - t) + warm.b() as f32 * t) as u8;
    Color32::from_rgb(r, g, b)
}

fn mode_accent_color(mode: &str) -> Color32 {
    match mode {
        "Conway's Game of Life" => Color32::from_rgb(0, 180, 220),
        "High Life"             => Color32::from_rgb(0, 210, 120),
        "Seeds"                 => Color32::from_rgb(220, 140, 40),
        "Day & Night"           => Color32::from_rgb(90, 120, 255),
        "Maze"                  => Color32::from_rgb(0, 170, 150),
        "Hexagonal Life"        => Color32::from_rgb(160, 80, 240),
        "Immigration Game"      => Color32::from_rgb(240, 160, 0),
        "Rainbow Game"          => Color32::from_rgb(240, 60, 120),
        "Langton's Ant"         => Color32::from_rgb(255, 120, 0),
        "Wireworld"             => Color32::from_rgb(255, 210, 0),
        "Brian's Brain"         => Color32::from_rgb(80, 140, 255),
        "Generations"           => Color32::from_rgb(0, 220, 180),
        "Custom Rules"          => Color32::from_rgb(180, 180, 180),
        _                       => Color32::GRAY,
    }
}

fn mode_short_description(mode: &str) -> &'static str {
    match mode {
        "Conway's Game of Life" => "Classic B3/S23 life-like automaton.",
        "High Life" => "B36/S23 variant known for replicators.",
        "Seeds" => "B2/S rule with fast explosive growth.",
        "Day & Night" => "Self-complementary B3678/S34678 rule.",
        "Maze" => "B3/S12345 rule that forms labyrinth patterns.",
        "Hexagonal Life" => "Life-like dynamics on a hex-neighbour grid.",
        "Immigration Game" => "Two-species Conway competition.",
        "Rainbow Game" => "Multi-color competitive Conway variant.",
        "Langton's Ant" => "Turmite with emergent highways.",
        "Wireworld" => "4-state cellular circuit simulator.",
        "Brian's Brain" => "3-state firing and refractory dynamics.",
        "Generations" => "Life-like births with multi-step decay.",
        "Custom Rules" => "Enter your own B/S rule.",
        _ => "",
    }
}

// ---------------------------------------------------------------------------
// RLE clipboard import
// ---------------------------------------------------------------------------

/// Parse an RLE-encoded pattern string into (dx, dy) offsets from (0, 0).
/// Supports the standard 2-state RLE format used by Golly and LifeWiki.
fn parse_rle(rle: &str) -> Vec<(i32, i32)> {
    let mut pts = Vec::new();
    // Concatenate all non-comment, non-header lines into one string.
    let data: String = rle
        .lines()
        .filter(|l| !l.starts_with('#') && !l.starts_with('x'))
        .collect::<Vec<_>>()
        .join("");
    let mut x: i32 = 0;
    let mut y: i32 = 0;
    let mut count_str = String::new();
    for ch in data.chars() {
        match ch {
            '0'..='9' => count_str.push(ch),
            'b' | '.' => {
                let n = count_str.parse::<i32>().unwrap_or(1);
                x += n;
                count_str.clear();
            }
            'o' | 'A'..='X' => {
                let n = count_str.parse::<i32>().unwrap_or(1);
                for dx in 0..n {
                    pts.push((x + dx, y));
                }
                x += n;
                count_str.clear();
            }
            '$' => {
                let n = count_str.parse::<i32>().unwrap_or(1);
                y += n;
                x = 0;
                count_str.clear();
            }
            '!' => break,
            ' ' | '\t' | '\r' | '\n' => {}
            _ => { count_str.clear(); }
        }
    }
    pts
}

// ---------------------------------------------------------------------------
// Application state
// ---------------------------------------------------------------------------

pub struct LifeGridApp {
    // ── Simulation ──────────────────────────────────────────────────────────
    automaton: Box<dyn Automaton>,
    undo: UndoManager,
    running: bool,
    generation: u64,
    last_step: Instant,

    // ── Settings ────────────────────────────────────────────────────────────
    speed: u32,
    cell_size: f32,
    show_grid: bool,
    dark_mode: bool,
    rounded_cells: bool,
    advanced_ui: bool,

    // ── Mode / pattern selectors ─────────────────────────────────────────────
    selected_mode: String,
    selected_pattern: String,
    selected_boundary: BoundaryMode,
    custom_rule_str: String,
    custom_birth: Vec<u8>,
    custom_survival: Vec<u8>,

    // ── Canvas ───────────────────────────────────────────────────────────────
    viewport_offset: Vec2,
    paint_state: u8,
    drag_undo_pushed: bool,
    fit_to_view_requested: bool,

    // ── Cell aging ───────────────────────────────────────────────────────────
    age_grid: Vec<u32>,
    show_aging: bool,

    // ── GIF recording ────────────────────────────────────────────────────────
    record_frames: bool,
    frame_buffer: Vec<Vec<u8>>,

    // ── Statistics ───────────────────────────────────────────────────────────
    pop_history: Vec<usize>,

    // ── Modals ───────────────────────────────────────────────────────────────
    show_run_n_dialog: bool,
    run_n_input: String,
    show_resize_dialog: bool,
    resize_w_input: String,
    resize_h_input: String,

    // ── FPS tracking ─────────────────────────────────────────────────────────
    last_frame_time: Instant,
    fps: f32,

    // ── Status bar ───────────────────────────────────────────────────────────
    status_msg: Option<(String, Instant)>,
    show_onboarding_hint: bool,
}

impl LifeGridApp {
    fn max_paint_state_for_mode(mode: &str) -> u8 {
        match mode {
            // Binary rules: only state 1 is considered alive.
            "Conway's Game of Life"
            | "High Life"
            | "Seeds"
            | "Day & Night"
            | "Maze"
            | "Hexagonal Life"
            | "Custom Rules"
            | "Langton's Ant" => 1,
            "Wireworld" => 3,
            "Brian's Brain" => 2,
            "Immigration Game" => 3,
            "Rainbow Game" => 6,
            // Generations defaults to 8 states (0..7).
            "Generations" => 7,
            _ => 1,
        }
    }

    fn max_paint_state(&self) -> u8 {
        Self::max_paint_state_for_mode(&self.selected_mode)
    }

    fn normalized_primary_paint_state(&self) -> u8 {
        self.paint_state.clamp(1, self.max_paint_state())
    }

    pub fn new(_cc: &eframe::CreationContext<'_>) -> Self {
        let cfg = AppConfig::load();

        let boundary = BoundaryMode::all()
            .iter()
            .copied()
            .find(|m| m.as_str() == cfg.boundary)
            .unwrap_or_default();

        let mut automaton = Self::make_auto(
            &cfg.automaton_mode,
            cfg.grid_width,
            cfg.grid_height,
            boundary,
            &cfg.custom_birth,
            &cfg.custom_survival,
        );

        let pattern = if automaton
            .available_patterns()
            .contains(&cfg.pattern.as_str())
        {
            cfg.pattern.clone()
        } else {
            automaton
                .available_patterns()
                .first()
                .copied()
                .unwrap_or("")
                .to_owned()
        };
        automaton.load_pattern(&pattern);

        let n = automaton.get_grid().cells.len();

        let custom_rule_str = {
            let b: String = cfg.custom_birth.iter().map(|n| n.to_string()).collect();
            let s: String = cfg.custom_survival.iter().map(|n| n.to_string()).collect();
            format!("B{}/S{}", b, s)
        };

        Self {
            automaton,
            undo: UndoManager::new(100),
            running: false,
            generation: 0,
            last_step: Instant::now(),

            speed: cfg.speed.clamp(1, 200),
            cell_size: cfg.cell_size.clamp(1.0, 64.0),
            show_grid: cfg.show_grid,
            dark_mode: cfg.dark_mode,
            rounded_cells: cfg.rounded_cells,
            advanced_ui: cfg.advanced_ui,

            selected_mode: cfg.automaton_mode,
            selected_pattern: pattern,
            selected_boundary: boundary,
            custom_rule_str,
            custom_birth: cfg.custom_birth,
            custom_survival: cfg.custom_survival,

            viewport_offset: Vec2::ZERO,
            paint_state: cfg.paint_state.max(1),
            drag_undo_pushed: false,
            fit_to_view_requested: false,

            age_grid: vec![0u32; n],
            show_aging: cfg.show_aging,

            record_frames: false,
            frame_buffer: Vec::new(),

            pop_history: Vec::new(),

            show_run_n_dialog: false,
            run_n_input: "100".into(),
            show_resize_dialog: false,
            resize_w_input: "100".into(),
            resize_h_input: "100".into(),

            last_frame_time: Instant::now(),
            fps: 0.0,

            status_msg: None,
            show_onboarding_hint: !cfg.first_run_complete,
        }
    }

    // ── Factory ─────────────────────────────────────────────────────────────

    fn make_auto(
        mode: &str,
        w: usize,
        h: usize,
        boundary: BoundaryMode,
        birth: &[u8],
        survival: &[u8],
    ) -> Box<dyn Automaton> {
        let mut auto: Box<dyn Automaton> = if mode == "Custom Rules" {
            Box::new(LifeLike::new(w, h, birth.to_vec(), survival.to_vec()))
        } else {
            automata::make_automaton(mode, w, h)
        };
        auto.set_boundary(boundary);
        auto
    }

    // ── Simulation helpers ───────────────────────────────────────────────────

    fn step_duration(&self) -> Duration {
        Duration::from_millis(1000 / self.speed.max(1) as u64)
    }

    fn do_step(&mut self) {
        self.automaton.step();
        self.generation += 1;

        // Snapshot cells before any further borrows.
        let (n, pop, cells) = {
            let g = self.automaton.get_grid();
            (g.cells.len(), g.population(), g.cells.clone())
        };

        // Update age grid.
        if self.age_grid.len() != n {
            self.age_grid = vec![0u32; n];
        }
        for i in 0..n {
            if cells[i] != 0 {
                self.age_grid[i] = self.age_grid[i].saturating_add(1);
            } else {
                self.age_grid[i] = 0;
            }
        }

        self.pop_history.push(pop);
        if self.pop_history.len() > 500 {
            self.pop_history.remove(0);
        }

        // GIF frame recording.
        if self.record_frames {
            self.frame_buffer.push(cells);
            if self.frame_buffer.len() > 500 {
                self.frame_buffer.remove(0);
            }
        }
    }

    fn do_reset(&mut self) {
        self.automaton.reset();
        self.generation = 0;
        self.pop_history.clear();
        self.running = false;
        let n = self.automaton.get_grid().cells.len();
        self.age_grid = vec![0u32; n];
        self.frame_buffer.clear();
    }

    fn randomize_grid(&mut self, alive_probability: f64) {
        self.push_undo();
        let mut rng = rand::thread_rng();
        let cells = &mut self.automaton.get_grid_mut().cells;
        for cell in cells.iter_mut() {
            *cell = if rng.gen_bool(alive_probability.clamp(0.0, 1.0)) { 1 } else { 0 };
        }
        self.generation = 0;
        self.running = false;
        self.pop_history.clear();
        self.frame_buffer.clear();
        if self.age_grid.len() != cells.len() {
            self.age_grid = vec![0u32; cells.len()];
        } else {
            self.age_grid.fill(0);
        }
    }

    fn clear_grid(&mut self) {
        self.push_undo();
        let cells = &mut self.automaton.get_grid_mut().cells;
        for cell in cells.iter_mut() {
            *cell = 0;
        }
        self.generation = 0;
        self.running = false;
        self.pop_history.clear();
        self.frame_buffer.clear();
        if self.age_grid.len() != cells.len() {
            self.age_grid = vec![0u32; cells.len()];
        } else {
            self.age_grid.fill(0);
        }
    }

    fn save_snapshot(&mut self) {
        let ts = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .map(|d| d.as_secs())
            .unwrap_or(0);
        let base = std::env::var("HOME")
            .map(std::path::PathBuf::from)
            .unwrap_or_else(|_| std::path::PathBuf::from("."));
        let dir = base.join("Pictures").join("LifeGrid");
        if let Err(e) = std::fs::create_dir_all(&dir) {
            self.set_status(format!("Snapshot failed: {}", e));
            return;
        }
        let path = dir.join(format!("lifegrid-{}.png", ts));
        let cs = (self.cell_size as u32).max(1);
        match export::export_png(self.automaton.get_grid(), cs, &path) {
            Ok(()) => self.set_status(format!("Snapshot saved: {}", path.display())),
            Err(e) => self.set_status(format!("Snapshot failed: {}", e)),
        }
    }

    fn mark_onboarded(&mut self) {
        self.show_onboarding_hint = false;
    }

    fn rebuild_automaton(&mut self) {
        let (w, h) = {
            let g = self.automaton.get_grid();
            (g.width, g.height)
        };
        let mut new_auto = Self::make_auto(
            &self.selected_mode,
            w,
            h,
            self.selected_boundary,
            &self.custom_birth,
            &self.custom_survival,
        );
        let patterns = new_auto.available_patterns();
        if !patterns.contains(&self.selected_pattern.as_str()) {
            self.selected_pattern = patterns.first().copied().unwrap_or("").to_owned();
        }
        new_auto.load_pattern(&self.selected_pattern);
        let n = new_auto.get_grid().cells.len();
        self.automaton = new_auto;
        self.paint_state = self.paint_state.clamp(1, self.max_paint_state());
        self.generation = 0;
        self.pop_history.clear();
        self.running = false;
        self.undo.clear();
        self.age_grid = vec![0u32; n];
        self.frame_buffer.clear();
        self.viewport_offset = Vec2::ZERO;
    }

    fn push_undo(&mut self) {
        let snapshot = self.automaton.get_grid().cells.clone();
        self.undo.push(snapshot);
    }

    fn set_status(&mut self, msg: impl Into<String>) {
        self.status_msg = Some((msg.into(), Instant::now()));
    }

    fn save_config(&self) {
        let grid = self.automaton.get_grid();
        let cfg = AppConfig {
            grid_width: grid.width,
            grid_height: grid.height,
            cell_size: self.cell_size,
            speed: self.speed,
            show_grid: self.show_grid,
            dark_mode: self.dark_mode,
            rounded_cells: self.rounded_cells,
            panel_width: 220.0,
            automaton_mode: self.selected_mode.clone(),
            pattern: self.selected_pattern.clone(),
            boundary: self.selected_boundary.as_str().to_owned(),
            custom_birth: self.custom_birth.clone(),
            custom_survival: self.custom_survival.clone(),
            paint_state: self.paint_state,
            show_aging: self.show_aging,
            advanced_ui: self.advanced_ui,
            first_run_complete: !self.show_onboarding_hint,
        };
        cfg.save();
    }

    // ── Theme ────────────────────────────────────────────────────────────────

    fn apply_theme(&self, ctx: &egui::Context) {
        if self.dark_mode {
            ctx.set_visuals(egui::Visuals::dark());
        } else {
            ctx.set_visuals(egui::Visuals::light());
        }
    }

    // ── Keyboard shortcuts ───────────────────────────────────────────────────

    fn handle_keyboard(&mut self, ctx: &egui::Context) {
        // Skip shortcuts when a text field is focused (e.g., custom rule input).
        if ctx.wants_keyboard_input() {
            return;
        }
        ctx.input(|i| {
            if i.key_pressed(egui::Key::Space) {
                self.running = !self.running;
                if self.running { self.last_step = Instant::now(); }
                self.mark_onboarded();
            }
            if i.key_pressed(egui::Key::S) {
                self.push_undo();
                self.do_step();
                self.mark_onboarded();
            }
            if i.key_pressed(egui::Key::R) {
                self.do_reset();
                let pat = self.selected_pattern.clone();
                self.automaton.load_pattern(&pat);
                self.mark_onboarded();
            }
            if i.key_pressed(egui::Key::G) {
                self.show_grid = !self.show_grid;
            }
            if i.modifiers.ctrl && i.key_pressed(egui::Key::Z) {
                let current = self.automaton.get_grid().cells.clone();
                if let Some(prev) = self.undo.undo(current) {
                    self.automaton.get_grid_mut().cells = prev;
                    if self.generation > 0 { self.generation -= 1; }
                }
            }
            if i.modifiers.ctrl
                && (i.key_pressed(egui::Key::Y)
                    || (i.modifiers.shift && i.key_pressed(egui::Key::Z)))
            {
                let current = self.automaton.get_grid().cells.clone();
                if let Some(next) = self.undo.redo(current) {
                    self.automaton.get_grid_mut().cells = next;
                    self.generation += 1;
                }
            }
            if i.modifiers.ctrl && i.key_pressed(egui::Key::S) {
                // Export PNG via keyboard shortcut (non-blocking open below)
                self.status_msg = Some(("Use Export PNG… button".into(), Instant::now()));
            }
            // Zoom
            let plus =
                i.key_pressed(egui::Key::Plus) || i.key_pressed(egui::Key::Equals);
            let minus = i.key_pressed(egui::Key::Minus);
            if plus  { self.cell_size = (self.cell_size + 1.0).min(64.0); }
            if minus { self.cell_size = (self.cell_size - 1.0).max(1.0); }
        });
    }

    // ── UI panels ────────────────────────────────────────────────────────────

    fn ui_toolbar(&mut self, ui: &mut egui::Ui) {
        ui.vertical(|ui| {
            ui.horizontal(|ui| {
                // Play / Pause
                let play_label = if self.running { "Pause" } else { "Play" };
                let play_hint  = if self.running { "Pause  (Space)" } else { "Play  (Space)" };
                if ui.button(play_label).on_hover_text(play_hint).clicked() {
                    self.running = !self.running;
                    if self.running { self.last_step = Instant::now(); }
                    self.mark_onboarded();
                }
                if ui.button("Step").on_hover_text("Advance one generation  (S)").clicked() {
                    self.push_undo();
                    self.do_step();
                    self.mark_onboarded();
                }
                if ui.button("Reset").on_hover_text("Reset to initial pattern  (R)").clicked() {
                    self.do_reset();
                    let pat = self.selected_pattern.clone();
                    self.automaton.load_pattern(&pat);
                    self.mark_onboarded();
                }

                ui.separator();

                // Undo / Redo
                let can_undo = self.undo.can_undo();
                let can_redo = self.undo.can_redo();
                if ui.add_enabled(can_undo, egui::Button::new("Undo"))
                    .on_hover_text("Undo  (Ctrl+Z)").clicked()
                {
                    let cur = self.automaton.get_grid().cells.clone();
                    if let Some(prev) = self.undo.undo(cur) {
                        self.automaton.get_grid_mut().cells = prev;
                        if self.generation > 0 { self.generation -= 1; }
                    }
                    self.mark_onboarded();
                }
                if ui.add_enabled(can_redo, egui::Button::new("Redo"))
                    .on_hover_text("Redo  (Ctrl+Y)").clicked()
                {
                    let cur = self.automaton.get_grid().cells.clone();
                    if let Some(next) = self.undo.redo(cur) {
                        self.automaton.get_grid_mut().cells = next;
                        self.generation += 1;
                    }
                    self.mark_onboarded();
                }

                ui.separator();

                if ui.button("Run N…").on_hover_text("Run a fixed number of steps").clicked() {
                    self.show_run_n_dialog = true;
                    self.mark_onboarded();
                }

                // Right side
                ui.with_layout(egui::Layout::right_to_left(egui::Align::Center), |ui| {
                    ui.label(
                        egui::RichText::new(format!("v{}", env!("CARGO_PKG_VERSION")))
                            .small()
                            .weak(),
                    );
                    ui.separator();
                    let mode_label = if self.advanced_ui { "Beginner" } else { "Advanced" };
                    if ui.button(mode_label).on_hover_text("Toggle UI complexity").clicked() {
                        self.advanced_ui = !self.advanced_ui;
                    }
                    ui.separator();
                    let theme_label = if self.dark_mode { "Light" } else { "Dark" };
                    if ui.button(theme_label).on_hover_text("Toggle theme").clicked() {
                        self.dark_mode = !self.dark_mode;
                    }
                });
            });

            ui.horizontal_wrapped(|ui| {
                if ui.small_button("Randomize").clicked() {
                    self.randomize_grid(0.20);
                    self.set_status("Randomized grid");
                    self.mark_onboarded();
                }
                if ui.small_button("Center View").clicked() {
                    self.viewport_offset = Vec2::ZERO;
                }
                if ui.small_button("Fit Grid").clicked() {
                    self.fit_to_view_requested = true;
                }
                if ui.small_button("Clear").clicked() {
                    self.clear_grid();
                    self.set_status("Grid cleared");
                    self.mark_onboarded();
                }
                if ui.small_button("Snapshot").clicked() {
                    self.save_snapshot();
                }
            });
        });
    }

    fn ui_statusbar(&mut self, ui: &mut egui::Ui) {
        ui.horizontal(|ui| {
            let pop = {
                let g = self.automaton.get_grid();
                g.population()
            };

            let run_state = if self.running { "Running" } else { "Paused" };

            ui.label(format!("{}", run_state));
            ui.separator();
            ui.label(format!("Gen {}", self.generation));
            ui.separator();
            ui.label(format!("Pop {}", pop));
            ui.separator();
            ui.label(format!("Speed {} /s", self.speed));
            ui.separator();
            ui.label(format!("Boundary {}", self.selected_boundary.as_str()));

            // Timed status message
            if let Some((ref msg, ts)) = self.status_msg.clone() {
                if ts.elapsed() < Duration::from_secs(4) {
                    ui.separator();
                    ui.colored_label(Color32::from_rgb(100, 220, 100), msg);
                } else {
                    self.status_msg = None;
                }
            }
        });
    }

    fn ui_controls(&mut self, ui: &mut egui::Ui) {
        // ── Automaton section ────────────────────────────────────────────────
        egui::CollapsingHeader::new("Automaton")
            .default_open(true)
            .show(ui, |ui| {
                egui::Grid::new("automaton_grid")
                    .num_columns(2)
                    .spacing([6.0, 4.0])
                    .show(ui, |ui| {
                        // Mode
                        ui.label("Mode");
                        let old_mode = self.selected_mode.clone();
                        egui::ComboBox::from_id_salt("mode_combo")
                            .selected_text(&self.selected_mode)
                            .width(ui.available_width())
                            .show_ui(ui, |ui| {
                                for &m in automata::ALL_MODES {
                                    ui.selectable_value(&mut self.selected_mode, m.to_owned(), m);
                                }
                            });
                        if self.selected_mode != old_mode {
                            self.rebuild_automaton();
                        }
                        ui.end_row();

                        ui.label("");
                        ui.label(
                            egui::RichText::new(mode_short_description(&self.selected_mode))
                                .small()
                                .weak(),
                        );
                        ui.end_row();

                        // Pattern
                        ui.label("Pattern");
                        let patterns: Vec<&str> = self.automaton.available_patterns().to_vec();
                        let old_pat = self.selected_pattern.clone();
                        egui::ComboBox::from_id_salt("pattern_combo")
                            .selected_text(&self.selected_pattern)
                            .width(ui.available_width())
                            .show_ui(ui, |ui| {
                                for &p in &patterns {
                                    ui.selectable_value(&mut self.selected_pattern, p.to_owned(), p);
                                }
                            });
                        if self.selected_pattern != old_pat {
                            self.do_reset();
                            let pat = self.selected_pattern.clone();
                            self.automaton.load_pattern(&pat);
                        }
                        ui.end_row();

                        // Boundary
                        ui.label("Boundary");
                        let old_bnd = self.selected_boundary;
                        egui::ComboBox::from_id_salt("boundary_combo")
                            .selected_text(self.selected_boundary.as_str())
                            .width(ui.available_width())
                            .show_ui(ui, |ui| {
                                for &b in BoundaryMode::all() {
                                    ui.selectable_value(&mut self.selected_boundary, b, b.as_str());
                                }
                            });
                        if self.selected_boundary != old_bnd {
                            self.automaton.set_boundary(self.selected_boundary);
                            self.set_status(format!(
                                "Boundary set to {}.",
                                self.selected_boundary.as_str()
                            ));
                        }
                        ui.end_row();

                        ui.label("");
                        ui.label(egui::RichText::new("Tip: Wrap is best for sustained evolution.").small().weak());
                        ui.end_row();
                    }); // end Grid

                // Custom rule editor
                if self.advanced_ui && self.selected_mode == "Custom Rules" {
                    ui.add_space(2.0);
                    ui.label("Rule (B/S notation):");
                    let old_rule = self.custom_rule_str.clone();
                    ui.text_edit_singleline(&mut self.custom_rule_str);
                    if self.custom_rule_str != old_rule {
                        let (b, s) = LifeLike::parse_bs(&self.custom_rule_str);
                        self.custom_birth = b;
                        self.custom_survival = s;
                        self.rebuild_automaton();
                    }
                }

                ui.add_space(4.0);
                ui.horizontal(|ui| {
                    if ui.button("Resize Grid…").clicked() {
                        let (gw, gh) = {
                            let g = self.automaton.get_grid();
                            (g.width, g.height)
                        };
                        self.resize_w_input = gw.to_string();
                        self.resize_h_input = gh.to_string();
                        self.show_resize_dialog = true;
                    }
                    if ui.button("Import RLE").on_hover_text("Paste RLE pattern from clipboard").clicked() {
                    match arboard::Clipboard::new()
                        .and_then(|mut c| c.get_text())
                    {
                        Ok(text) => {
                            let pts = parse_rle(&text);
                            if pts.is_empty() {
                                self.set_status("Clipboard: no valid RLE found");
                            } else {
                                let (gw, gh) = {
                                    let g = self.automaton.get_grid();
                                    (g.width as i32, g.height as i32)
                                };
                                let cx = gw / 2;
                                let cy = gh / 2;
                                self.push_undo();
                                for (dx, dy) in pts {
                                    let x = cx + dx;
                                    let y = cy + dy;
                                    if x >= 0 && x < gw && y >= 0 && y < gh {
                                        self.automaton
                                            .get_grid_mut()
                                            .set(y as usize, x as usize, 1);
                                    }
                                }
                                self.set_status("RLE pattern imported");
                            }
                        }
                        Err(e) => self.set_status(format!("Clipboard error: {e}")),
                    }
                }
                }); // end horizontal (Resize / Import)
            });

        ui.add_space(4.0);

        // ── View section ─────────────────────────────────────────────────────
        egui::CollapsingHeader::new("View")
            .default_open(true)
            .show(ui, |ui| {
                egui::Grid::new("view_grid")
                    .num_columns(2)
                    .spacing([6.0, 4.0])
                    .show(ui, |ui| {
                        ui.label("Speed");
                        ui.add(egui::Slider::new(&mut self.speed, 1..=200).suffix(" /s"));
                        ui.end_row();

                        ui.label("Cell size");
                        ui.add(egui::Slider::new(&mut self.cell_size, 1.0..=64.0).suffix(" px"));
                        ui.end_row();

                        if self.advanced_ui {
                            ui.label("Paint state");
                            let max_state = self.max_paint_state();
                            ui.add(egui::Slider::new(&mut self.paint_state, 0..=max_state)
                                .clamping(egui::SliderClamping::Always));
                            ui.end_row();
                        }
                    });

                ui.add_space(2.0);
                ui.checkbox(&mut self.show_grid, "Grid lines");
                if self.advanced_ui {
                    egui::CollapsingHeader::new("Advanced display")
                        .default_open(false)
                        .show(ui, |ui| {
                            ui.checkbox(&mut self.rounded_cells, "Rounded cells");
                            ui.checkbox(&mut self.show_aging, "Cell aging");
                        });
                }
            });

        if self.advanced_ui {
            ui.add_space(4.0);

            // ── Statistics section ───────────────────────────────────────────────
            egui::CollapsingHeader::new("Statistics")
                .default_open(false)
                .show(ui, |ui| {
                if self.pop_history.len() > 1 {
                    let max_pop = self
                        .pop_history
                        .iter()
                        .copied()
                        .max()
                        .unwrap_or(1)
                        .max(1);
                    let min_pop = self.pop_history.iter().copied().min().unwrap_or(0);
                    let avg_pop = self.pop_history.iter().sum::<usize>()
                        / self.pop_history.len();

                    ui.label(format!("Peak: {}  Min: {}  Avg: {}", max_pop, min_pop, avg_pop));

                    // Sparkline
                    let graph_size = Vec2::new(ui.available_width(), 56.0);
                    let (rect, _) = ui.allocate_exact_size(graph_size, Sense::hover());
                    let painter = ui.painter_at(rect);
                    let bg = if self.dark_mode {
                        Color32::from_rgb(20, 20, 30)
                    } else {
                        Color32::from_gray(240)
                    };
                    painter.rect_filled(rect, CornerRadius::same(3), bg);
                    let n = self.pop_history.len();
                    let step = rect.width() / n.max(2) as f32;
                    let accent = mode_accent_color(&self.selected_mode);
                    let pts: Vec<egui::Pos2> = self
                        .pop_history
                        .iter()
                        .enumerate()
                        .map(|(i, &p)| {
                            egui::pos2(
                                rect.left() + i as f32 * step,
                                rect.bottom()
                                    - (p as f32 / max_pop as f32) * (rect.height() - 4.0)
                                    - 2.0,
                            )
                        })
                        .collect();
                    painter.add(egui::Shape::line(pts, egui::Stroke::new(1.5, accent)));
                } else {
                    ui.weak("Run the simulation to see statistics.");
                }

                if ui.small_button("Reset stats").clicked() {
                    self.pop_history.clear();
                }
            });

            ui.add_space(4.0);

            // ── Export section ───────────────────────────────────────────────────
            egui::CollapsingHeader::new("Export")
                .default_open(false)
                .show(ui, |ui| {
                if ui.button("Export PNG…").clicked() {
                    if let Some(path) = rfd::FileDialog::new()
                        .add_filter("PNG image", &["png"])
                        .save_file()
                    {
                        let cs = (self.cell_size as u32).max(1);
                        match export::export_png(self.automaton.get_grid(), cs, &path) {
                            Ok(()) => self.set_status(format!("Saved {}", path.display())),
                            Err(e) => self.set_status(format!("Export failed: {}", e)),
                        }
                    }
                }

                ui.separator();

                ui.checkbox(&mut self.record_frames, "Record frames");
                if self.record_frames {
                    ui.label(
                        egui::RichText::new(format!(
                            "{} frames buffered (max 500)",
                            self.frame_buffer.len()
                        ))
                        .small(),
                    );
                }
                if ui
                    .add_enabled(!self.frame_buffer.is_empty(), egui::Button::new("Export GIF…"))
                    .clicked()
                {
                    if let Some(path) = rfd::FileDialog::new()
                        .add_filter("GIF animation", &["gif"])
                        .save_file()
                    {
                        let (gw, gh) = {
                            let g = self.automaton.get_grid();
                            (g.width, g.height)
                        };
                        let cs = (self.cell_size as u32).max(1).min(8);
                        let delay = 1000 / self.speed.clamp(1, 30);
                        match export::export_gif(
                            &self.frame_buffer,
                            gw,
                            gh,
                            cs,
                            delay,
                            &path,
                        ) {
                            Ok(()) => self.set_status(format!(
                                "GIF saved ({} frames)",
                                self.frame_buffer.len()
                            )),
                            Err(e) => self.set_status(format!("GIF failed: {}", e)),
                        }
                    }
                }
                if ui
                    .add_enabled(!self.frame_buffer.is_empty(), egui::Button::new("Clear frames"))
                    .clicked()
                {
                    self.frame_buffer.clear();
                    self.set_status("Frame buffer cleared");
                }
            });
        }
    }

    fn ui_canvas(&mut self, ui: &mut egui::Ui) {
        let avail = ui.available_size();
        let (rect, response) =
            ui.allocate_exact_size(avail, Sense::click_and_drag());

        let cs = self.cell_size;
        let dark = self.dark_mode;
        let show_grid = self.show_grid;
        let show_aging = self.show_aging;
        let rounding = if self.rounded_cells {
            CornerRadius::same(((cs * 0.18).max(1.0)) as u8)
        } else {
            CornerRadius::ZERO
        };

        let (gw, gh, cells_snapshot, age_snapshot) = {
            let g = self.automaton.get_grid();
            (g.width, g.height, g.cells.clone(), self.age_grid.clone())
        };

        if self.fit_to_view_requested {
            let sx = avail.x / gw.max(1) as f32;
            let sy = avail.y / gh.max(1) as f32;
            self.cell_size = sx.min(sy).clamp(1.0, 64.0);
            self.viewport_offset = Vec2::ZERO;
            self.fit_to_view_requested = false;
        }

        // ── Mouse-wheel zoom ─────────────────────────────────────────────────
        if response.hovered() {
            let scroll_y = ui.ctx().input(|i| i.smooth_scroll_delta.y);
            if scroll_y.abs() > 0.1 {
                let old_cs = self.cell_size;
                let new_cs = (old_cs * (1.0 + scroll_y * 0.04)).clamp(1.0, 64.0);
                if let Some(cursor) = ui.ctx().input(|i| i.pointer.hover_pos()) {
                    let rel = (cursor - rect.min) + self.viewport_offset;
                    self.viewport_offset = rel * (new_cs / old_cs) - (cursor - rect.min);
                }
                self.cell_size = new_cs;
            }
        }

        // ── Middle-click pan ─────────────────────────────────────────────────
        if response.dragged_by(egui::PointerButton::Middle) {
            self.viewport_offset -= response.drag_delta();
        }

        // Clamp viewport to grid bounds.
        let max_vx = (gw as f32 * self.cell_size - avail.x).max(0.0);
        let max_vy = (gh as f32 * self.cell_size - avail.y).max(0.0);
        self.viewport_offset.x = self.viewport_offset.x.clamp(0.0, max_vx);
        self.viewport_offset.y = self.viewport_offset.y.clamp(0.0, max_vy);

        let vox = self.viewport_offset.x;
        let voy = self.viewport_offset.y;
        let cs = self.cell_size; // re-read after zoom

        // ── Visible cell culling ─────────────────────────────────────────────
        let start_gx = ((vox / cs) as i64 - 1).max(0) as usize;
        let end_gx = (((vox + avail.x) / cs) as i64 + 2).min(gw as i64) as usize;
        let start_gy = ((voy / cs) as i64 - 1).max(0) as usize;
        let end_gy = (((voy + avail.y) / cs) as i64 + 2).min(gh as i64) as usize;

        let painter = ui.painter_at(rect);

        // ── Background ───────────────────────────────────────────────────────
        let bg = cell_color(0, dark);
        painter.rect_filled(rect, CornerRadius::ZERO, bg);

        // ── Cells ────────────────────────────────────────────────────────────
        for gy in start_gy..end_gy {
            for gx in start_gx..end_gx {
                let state = cells_snapshot[gy * gw + gx];
                if state == 0 {
                    continue;
                }
                let base = cell_color(state, dark);
                let color = if show_aging && !age_snapshot.is_empty() {
                    aging_color(base, age_snapshot[gy * gw + gx])
                } else {
                    base
                };
                let cell_rect = Rect::from_min_size(
                    egui::pos2(rect.left() - vox + gx as f32 * cs, rect.top() - voy + gy as f32 * cs),
                    Vec2::splat(cs),
                );
                painter.rect_filled(cell_rect, rounding, color);
            }
        }

        // ── Grid lines ───────────────────────────────────────────────────────
        if show_grid && cs >= 4.0 {
            let lc = if dark { Color32::from_gray(50) } else { Color32::from_gray(210) };
            let stroke = egui::Stroke::new(0.5, lc);
            for gx in start_gx..=end_gx {
                let px = rect.left() - vox + gx as f32 * cs;
                if px >= rect.left() - 1.0 && px <= rect.right() + 1.0 {
                    painter.line_segment(
                        [egui::pos2(px, rect.top()), egui::pos2(px, rect.bottom())],
                        stroke,
                    );
                }
            }
            for gy in start_gy..=end_gy {
                let py = rect.top() - voy + gy as f32 * cs;
                if py >= rect.top() - 1.0 && py <= rect.bottom() + 1.0 {
                    painter.line_segment(
                        [egui::pos2(rect.left(), py), egui::pos2(rect.right(), py)],
                        stroke,
                    );
                }
            }
        }

        // ── Hover highlight ──────────────────────────────────────────────────
        let accent = mode_accent_color(&self.selected_mode);
        if let Some(cursor) = response.hover_pos() {
            let hx = ((cursor.x - rect.left() + vox) / cs) as i64;
            let hy = ((cursor.y - rect.top() + voy) / cs) as i64;
            if hx >= 0 && hx < gw as i64 && hy >= 0 && hy < gh as i64 {
                let hover_rect = Rect::from_min_size(
                    egui::pos2(
                        rect.left() - vox + hx as f32 * cs,
                        rect.top() - voy + hy as f32 * cs,
                    ),
                    Vec2::splat(cs),
                );
                let state = cells_snapshot[hy as usize * gw + hx as usize];
                let hl = Color32::from_rgba_premultiplied(
                    accent.r() / 3,
                    accent.g() / 3,
                    accent.b() / 3,
                    60,
                );
                painter.rect_filled(hover_rect, rounding, hl);
                response.clone().on_hover_text(format!(
                    "({}, {})  state: {}",
                    hx, hy, state
                ));
            }
        }

        // ── Left-click / drag: paint ─────────────────────────────────────────
        if response.dragged_by(egui::PointerButton::Primary) || response.clicked() {
            if let Some(pos) = response.interact_pointer_pos() {
                let gx = ((pos.x - rect.left() + vox) / cs) as i64;
                let gy_v = ((pos.y - rect.top() + voy) / cs) as i64;
                if gx >= 0 && gx < gw as i64 && gy_v >= 0 && gy_v < gh as i64 {
                    self.mark_onboarded();
                    if !self.drag_undo_pushed {
                        self.push_undo();
                        self.drag_undo_pushed = true;
                    }
                    let paint = self.normalized_primary_paint_state();
                    self.automaton
                        .paint_cell(gx as usize, gy_v as usize, paint);
                }
            }
        }

        // ── Right-click / drag: erase ─────────────────────────────────────────
        if response.dragged_by(egui::PointerButton::Secondary)
            || response.secondary_clicked()
        {
            if let Some(pos) = response.interact_pointer_pos() {
                let gx = ((pos.x - rect.left() + vox) / cs) as i64;
                let gy_v = ((pos.y - rect.top() + voy) / cs) as i64;
                if gx >= 0 && gx < gw as i64 && gy_v >= 0 && gy_v < gh as i64 {
                    self.mark_onboarded();
                    if !self.drag_undo_pushed {
                        self.push_undo();
                        self.drag_undo_pushed = true;
                    }
                    self.automaton
                        .paint_cell(gx as usize, gy_v as usize, 0);
                }
            }
        }

        // Reset drag-undo sentinel when not dragging.
        if !response.dragged() {
            self.drag_undo_pushed = false;
        }

        if !self.running && self.generation == 0 {
            let helper = "Click to draw, then press Play. Use Randomize for a quick start.";
            painter.text(
                rect.center_top() + Vec2::new(0.0, 12.0),
                egui::Align2::CENTER_TOP,
                helper,
                egui::FontId::proportional(13.0),
                if dark { Color32::from_gray(170) } else { Color32::from_gray(90) },
            );
        }

        if self.show_onboarding_hint {
            let msg = "Tip: Start with Play, Step, or Randomize. Switch to Advanced for more controls.";
            painter.text(
                rect.center_bottom() - Vec2::new(0.0, 14.0),
                egui::Align2::CENTER_BOTTOM,
                msg,
                egui::FontId::proportional(13.0),
                if dark { Color32::from_rgb(185, 205, 255) } else { Color32::from_rgb(30, 80, 150) },
            );
        }
    }

    // ── Modal dialogs ────────────────────────────────────────────────────────

    fn ui_run_n_dialog(&mut self, ctx: &egui::Context) {
        if !self.show_run_n_dialog {
            return;
        }
        let mut open = true;
        egui::Window::new("Run N Steps")
            .collapsible(false)
            .resizable(false)
            .anchor(egui::Align2::CENTER_CENTER, Vec2::ZERO)
            .open(&mut open)
            .show(ctx, |ui| {
                ui.label("Number of steps:");
                ui.text_edit_singleline(&mut self.run_n_input);
                ui.horizontal(|ui| {
                    if ui.button("Run").clicked() {
                        if let Ok(n) = self.run_n_input.trim().parse::<u64>() {
                            let n = n.min(100_000);
                            for _ in 0..n {
                                self.do_step();
                            }
                            self.set_status(format!("Ran {} steps", n));
                        }
                        self.show_run_n_dialog = false;
                    }
                    if ui.button("Cancel").clicked() {
                        self.show_run_n_dialog = false;
                    }
                });
            });
        if !open {
            self.show_run_n_dialog = false;
        }
    }

    fn ui_resize_dialog(&mut self, ctx: &egui::Context) {
        if !self.show_resize_dialog {
            return;
        }
        let mut open = true;
        egui::Window::new("Resize Grid")
            .collapsible(false)
            .resizable(false)
            .anchor(egui::Align2::CENTER_CENTER, Vec2::ZERO)
            .open(&mut open)
            .show(ctx, |ui| {
                ui.horizontal(|ui| {
                    ui.label("Width:");
                    ui.text_edit_singleline(&mut self.resize_w_input);
                });
                ui.horizontal(|ui| {
                    ui.label("Height:");
                    ui.text_edit_singleline(&mut self.resize_h_input);
                });
                ui.horizontal(|ui| {
                    if ui.button("Resize").clicked() {
                        let w = self.resize_w_input.trim().parse::<usize>().unwrap_or(100).clamp(10, 1000);
                        let h = self.resize_h_input.trim().parse::<usize>().unwrap_or(100).clamp(10, 1000);
                        let mut new_auto = Self::make_auto(
                            &self.selected_mode,
                            w,
                            h,
                            self.selected_boundary,
                            &self.custom_birth,
                            &self.custom_survival,
                        );
                        new_auto.load_pattern(&self.selected_pattern);
                        let n = new_auto.get_grid().cells.len();
                        self.automaton = new_auto;
                        self.generation = 0;
                        self.pop_history.clear();
                        self.running = false;
                        self.undo.clear();
                        self.age_grid = vec![0u32; n];
                        self.frame_buffer.clear();
                        self.viewport_offset = Vec2::ZERO;
                        self.set_status(format!("Grid resized to {}×{}", w, h));
                        self.show_resize_dialog = false;
                    }
                    if ui.button("Cancel").clicked() {
                        self.show_resize_dialog = false;
                    }
                });
            });
        if !open {
            self.show_resize_dialog = false;
        }
    }
}

// ---------------------------------------------------------------------------
// eframe::App
// ---------------------------------------------------------------------------

impl eframe::App for LifeGridApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        // Apply theme
        self.apply_theme(ctx);

        // FPS tracking (exponential moving average)
        let now = Instant::now();
        let dt = now.duration_since(self.last_frame_time).as_secs_f32();
        if dt > 0.0 {
            self.fps = self.fps * 0.9 + (1.0 / dt) * 0.1;
        }
        self.last_frame_time = now;

        // Keyboard shortcuts
        self.handle_keyboard(ctx);

        // Simulation tick
        if self.running {
            let step_dur = self.step_duration();
            let now = Instant::now();
            if now - self.last_step >= step_dur {
                self.do_step();
                self.last_step = now;
            }
            ctx.request_repaint_after(step_dur);
        }

        // Modal dialogs (rendered above all panels)
        self.ui_run_n_dialog(ctx);
        self.ui_resize_dialog(ctx);

        // Toolbar
        egui::TopBottomPanel::top("toolbar")
            .frame(egui::Frame::side_top_panel(&ctx.style()))
            .show(ctx, |ui| {
                self.ui_toolbar(ui);
            });

        // Status bar
        egui::TopBottomPanel::bottom("statusbar")
            .frame(egui::Frame::side_top_panel(&ctx.style()))
            .show(ctx, |ui| {
                self.ui_statusbar(ui);
            });

        // Controls side panel
        egui::SidePanel::left("controls")
            .resizable(true)
            .min_width(180.0)
            .default_width(220.0)
            .show(ctx, |ui| {
                egui::ScrollArea::vertical().show(ui, |ui| {
                    self.ui_controls(ui);
                });
            });

        // Canvas
        egui::CentralPanel::default().show(ctx, |ui| {
            self.ui_canvas(ui);
        });
    }

    fn on_exit(&mut self, _gl: Option<&eframe::glow::Context>) {
        self.save_config();
    }
}
