import "./style.css";

import { ALL_MODELS, createModel } from "./automata/models";
import type { Automaton, BoundaryMode } from "./core/types";
import packageJson from "../package.json";

type State = {
  modelName: string;
  pattern: string;
  running: boolean;
  generation: number;
  speed: number;
  boundary: BoundaryMode;
  cellSize: number;
  viewportX: number;
  viewportY: number;
  model: Automaton;
  undoStack: Uint8Array[];
  redoStack: Uint8Array[];
  timer?: number;
};

type PersistedState = {
  modelName: string;
  pattern: string;
  speed: number;
  boundary: BoundaryMode;
  cellSize: number;
  viewportX: number;
  viewportY: number;
  generation: number;
  grid: string;
};

type MinimapInfo = {
  x: number;
  y: number;
  w: number;
  h: number;
};

const app = document.querySelector<HTMLDivElement>("#app");
if (!app) {
  throw new Error("App mount not found");
}

const STORAGE_KEY = "lifegrid-ts:session:v1";

app.innerHTML = `
  <main class="layout">
    <aside class="panel">
      <h1>LifeGrid TS <span class="version">v${packageJson.version}</span></h1>
      <p class="sub">TypeScript refactor of simulation core and UI loop.</p>

      <label>Model
        <select id="model"></select>
      </label>

      <label>Pattern
        <select id="pattern"></select>
      </label>

      <label>Speed <span id="speedValue"></span>
        <input id="speed" type="range" min="1" max="60" value="12" />
      </label>

      <label>Boundary
        <select id="boundary">
          <option value="wrap">Wrap</option>
          <option value="fixed">Fixed</option>
          <option value="reflect">Reflect</option>
        </select>
      </label>

      <label>Cell Size <span id="cellSizeValue"></span>
        <input id="cellSize" type="range" min="4" max="24" value="10" />
      </label>

      <div class="row">
        <button id="play">Play</button>
        <button id="step">Step</button>
        <button id="reset">Reset</button>
      </div>

      <div class="row">
        <button id="random">Randomize</button>
        <button id="clear">Clear</button>
      </div>

      <div class="row">
        <button id="undo">Undo</button>
        <button id="redo">Redo</button>
        <button id="exportPng">Export PNG</button>
      </div>

      <div class="row">
        <button id="centerView">Center</button>
        <button id="fitView">Fit</button>
      </div>

      <div class="row run-row">
        <input id="runN" type="number" min="1" max="5000" step="1" value="50" />
        <button id="runNButton">Run N</button>
      </div>

      <div class="row">
        <button id="saveState">Save</button>
        <button id="loadState">Load</button>
      </div>

      <div class="stats">
        <span>Gen <strong id="genValue">0</strong></span>
        <span>Pop <strong id="popValue">0</strong></span>
      </div>

      <p class="hint">Shortcuts: Space Play/Pause, S Step, R Reset, N Run-N.</p>

      <p id="status" class="status"></p>
    </aside>

    <section class="stage">
      <canvas id="canvas"></canvas>
    </section>
  </main>
`;

const canvasEl = document.querySelector<HTMLCanvasElement>("#canvas");
if (!canvasEl) {
  throw new Error("Canvas not available");
}
const ctxEl = canvasEl.getContext("2d");
if (!ctxEl) {
  throw new Error("Canvas context not available");
}
const canvas: HTMLCanvasElement = canvasEl;
const ctx: CanvasRenderingContext2D = ctxEl;
const stage = document.querySelector<HTMLElement>(".stage");
if (!stage) {
  throw new Error("Stage not available");
}
const stageEl: HTMLElement = stage;

const modelSelect = document.querySelector<HTMLSelectElement>("#model")!;
const patternSelect = document.querySelector<HTMLSelectElement>("#pattern")!;
const speedInput = document.querySelector<HTMLInputElement>("#speed")!;
const speedValue = document.querySelector<HTMLSpanElement>("#speedValue")!;
const boundarySelect = document.querySelector<HTMLSelectElement>("#boundary")!;
const cellSizeInput = document.querySelector<HTMLInputElement>("#cellSize")!;
const cellSizeValue = document.querySelector<HTMLSpanElement>("#cellSizeValue")!;
const playButton = document.querySelector<HTMLButtonElement>("#play")!;
const stepButton = document.querySelector<HTMLButtonElement>("#step")!;
const resetButton = document.querySelector<HTMLButtonElement>("#reset")!;
const randomButton = document.querySelector<HTMLButtonElement>("#random")!;
const clearButton = document.querySelector<HTMLButtonElement>("#clear")!;
const undoButton = document.querySelector<HTMLButtonElement>("#undo")!;
const redoButton = document.querySelector<HTMLButtonElement>("#redo")!;
const exportPngButton = document.querySelector<HTMLButtonElement>("#exportPng")!;
const centerViewButton = document.querySelector<HTMLButtonElement>("#centerView")!;
const fitViewButton = document.querySelector<HTMLButtonElement>("#fitView")!;
const runNInput = document.querySelector<HTMLInputElement>("#runN")!;
const runNButton = document.querySelector<HTMLButtonElement>("#runNButton")!;
const saveStateButton = document.querySelector<HTMLButtonElement>("#saveState")!;
const loadStateButton = document.querySelector<HTMLButtonElement>("#loadState")!;
const status = document.querySelector<HTMLParagraphElement>("#status")!;
const genValue = document.querySelector<HTMLSpanElement>("#genValue")!;
const popValue = document.querySelector<HTMLSpanElement>("#popValue")!;

const state: State = {
  modelName: "Conway",
  pattern: "Glider",
  running: false,
  generation: 0,
  speed: Number(speedInput.value),
  boundary: "wrap",
  cellSize: Number(cellSizeInput.value),
  viewportX: 0,
  viewportY: 0,
  model: createModel("Conway", 96, 72, "wrap"),
  undoStack: [],
  redoStack: [],
};

let dragPointerId: number | null = null;
let dragButton = 0;
let dragSnapshotPushed = false;
let panPointerId: number | null = null;
let panStartClientX = 0;
let panStartClientY = 0;
let panStartViewportX = 0;
let panStartViewportY = 0;
let minimap: MinimapInfo | null = null;

function setStatus(text: string): void {
  status.textContent = text;
}

function encodeCells(cells: Uint8Array): string {
  let binary = "";
  for (let i = 0; i < cells.length; i += 1) {
    binary += String.fromCharCode(cells[i]);
  }
  return btoa(binary);
}

function decodeCells(encoded: string): Uint8Array | null {
  try {
    const binary = atob(encoded);
    const out = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i += 1) {
      out[i] = binary.charCodeAt(i) & 0xff;
    }
    return out;
  } catch {
    return null;
  }
}

function makePersistedState(): PersistedState {
  return {
    modelName: state.modelName,
    pattern: state.pattern,
    speed: state.speed,
    boundary: state.boundary,
    cellSize: state.cellSize,
    viewportX: state.viewportX,
    viewportY: state.viewportY,
    generation: state.generation,
    grid: encodeCells(state.model.grid.cells),
  };
}

function persistState(): void {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(makePersistedState()));
}

function restorePersistedState(): boolean {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return false;
  }

  try {
    const parsed = JSON.parse(raw) as PersistedState;
    if (!ALL_MODELS.includes(parsed.modelName)) {
      return false;
    }

    state.modelName = parsed.modelName;
    state.boundary =
      parsed.boundary === "fixed"
        ? "fixed"
        : parsed.boundary === "reflect"
          ? "reflect"
          : "wrap";
    state.model = createModel(parsed.modelName, 96, 72, state.boundary);
    state.pattern = state.model.patterns.includes(parsed.pattern)
      ? parsed.pattern
      : (state.model.patterns[0] ?? "Random Soup");
    state.speed = Math.max(1, Math.min(60, parsed.speed));
    state.cellSize = Math.max(4, Math.min(24, parsed.cellSize));
    state.viewportX = Math.max(0, parsed.viewportX);
    state.viewportY = Math.max(0, parsed.viewportY);
    state.generation = Math.max(0, Math.floor(parsed.generation));
    state.running = false;
    state.undoStack = [];
    state.redoStack = [];

    const decoded = decodeCells(parsed.grid);
    if (decoded && decoded.length === state.model.grid.cells.length) {
      state.model.grid.cells.set(decoded);
    } else {
      state.model.loadPattern(state.pattern);
      state.generation = 0;
    }

    return true;
  } catch {
    return false;
  }
}

function fillSelect(select: HTMLSelectElement, values: string[], selected: string): void {
  select.innerHTML = values
    .map((v) => `<option value="${v}" ${v === selected ? "selected" : ""}>${v}</option>`)
    .join("");
}

function updateStats(): void {
  genValue.textContent = String(state.generation);
  popValue.textContent = String(state.model.grid.population());
}

function snapshotCells(): Uint8Array {
  return new Uint8Array(state.model.grid.cells);
}

function pushUndoSnapshot(): void {
  state.undoStack.push(snapshotCells());
  if (state.undoStack.length > 200) {
    state.undoStack.shift();
  }
  state.redoStack = [];
}

function restoreSnapshot(cells: Uint8Array): void {
  state.model.grid.cells.set(cells);
}

function applyUndo(): void {
  if (state.undoStack.length === 0) {
    setStatus("Nothing to undo.");
    return;
  }
  state.redoStack.push(snapshotCells());
  const prev = state.undoStack.pop();
  if (!prev) {
    return;
  }
  restoreSnapshot(prev);
  state.generation = Math.max(0, state.generation - 1);
  render();
  setStatus("Undo.");
  persistState();
}

function applyRedo(): void {
  if (state.redoStack.length === 0) {
    setStatus("Nothing to redo.");
    return;
  }
  state.undoStack.push(snapshotCells());
  const next = state.redoStack.pop();
  if (!next) {
    return;
  }
  restoreSnapshot(next);
  state.generation += 1;
  render();
  setStatus("Redo.");
  persistState();
}

function runNSteps(steps: number): void {
  if (!Number.isFinite(steps) || steps <= 0) {
    setStatus("Run N requires a positive number.");
    return;
  }

  pushUndoSnapshot();
  for (let i = 0; i < steps; i += 1) {
    state.model.step();
  }
  state.generation += steps;
  render();
  setStatus(`Ran ${steps} steps.`);
  persistState();
}

function exportPng(): void {
  const dataUrl = canvas.toDataURL("image/png");
  const a = document.createElement("a");
  const ts = new Date().toISOString().replace(/[:.]/g, "-");
  a.href = dataUrl;
  a.download = `lifegrid-ts-${state.modelName.replace(/\s+/g, "-").toLowerCase()}-${ts}.png`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setStatus("Exported PNG.");
}

function rebuildModel(): void {
  state.undoStack = [];
  state.redoStack = [];
  state.model = createModel(state.modelName, 96, 72, state.boundary);
  state.generation = 0;
  state.viewportX = 0;
  state.viewportY = 0;
  const defaultPattern = state.model.patterns[0] ?? "Random Soup";
  state.pattern = defaultPattern;
  fillSelect(patternSelect, state.model.patterns, state.pattern);
  state.model.loadPattern(state.pattern);
  render();
  setStatus(`Loaded ${state.modelName} (${state.pattern}).`);
  persistState();
}

function resizeCanvas(): void {
  const rect = stageEl.getBoundingClientRect();
  const width = Math.max(320, Math.floor(rect.width - 32));
  const height = Math.max(240, Math.floor(rect.height - 32));
  if (canvas.width !== width) {
    canvas.width = width;
  }
  if (canvas.height !== height) {
    canvas.height = height;
  }
}

function clampViewport(): void {
  const worldWidth = state.model.grid.width * state.cellSize;
  const worldHeight = state.model.grid.height * state.cellSize;
  const maxX = Math.max(0, worldWidth - canvas.width);
  const maxY = Math.max(0, worldHeight - canvas.height);
  state.viewportX = Math.max(0, Math.min(state.viewportX, maxX));
  state.viewportY = Math.max(0, Math.min(state.viewportY, maxY));
}

function centerView(): void {
  const worldWidth = state.model.grid.width * state.cellSize;
  const worldHeight = state.model.grid.height * state.cellSize;
  state.viewportX = (worldWidth - canvas.width) * 0.5;
  state.viewportY = (worldHeight - canvas.height) * 0.5;
  clampViewport();
  render();
}

function fitView(): void {
  const scaleX = canvas.width / Math.max(1, state.model.grid.width);
  const scaleY = canvas.height / Math.max(1, state.model.grid.height);
  state.cellSize = Math.max(4, Math.min(24, Math.floor(Math.min(scaleX, scaleY))));
  cellSizeInput.value = String(Math.round(state.cellSize));
  cellSizeValue.textContent = `${Math.round(state.cellSize)}px`;
  centerView();
}

function render(): void {
  resizeCanvas();
  clampViewport();
  ctx.fillStyle = "#0f1115";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  const startX = Math.max(0, Math.floor(state.viewportX / state.cellSize));
  const startY = Math.max(0, Math.floor(state.viewportY / state.cellSize));
  const endX = Math.min(
    state.model.grid.width,
    Math.ceil((state.viewportX + canvas.width) / state.cellSize),
  );
  const endY = Math.min(
    state.model.grid.height,
    Math.ceil((state.viewportY + canvas.height) / state.cellSize),
  );

  for (let y = startY; y < endY; y += 1) {
    for (let x = startX; x < endX; x += 1) {
      const cell = state.model.grid.get(x, y);
      if (cell === 0) {
        continue;
      }
      ctx.fillStyle = state.model.colorForState(cell);
      const px = x * state.cellSize - state.viewportX;
      const py = y * state.cellSize - state.viewportY;
      ctx.fillRect(px, py, state.cellSize - 1, state.cellSize - 1);
    }
  }

  drawMinimap();

  updateStats();
}

function drawMinimap(): void {
  const margin = 12;
  const mapW = Math.max(120, Math.min(200, Math.floor(canvas.width * 0.28)));
  const mapH = Math.max(90, Math.floor((mapW * state.model.grid.height) / state.model.grid.width));
  const x = canvas.width - mapW - margin;
  const y = canvas.height - mapH - margin;

  minimap = { x, y, w: mapW, h: mapH };

  ctx.fillStyle = "rgba(8, 12, 18, 0.85)";
  ctx.fillRect(x, y, mapW, mapH);
  ctx.strokeStyle = "rgba(255, 255, 255, 0.28)";
  ctx.lineWidth = 1;
  ctx.strokeRect(x + 0.5, y + 0.5, mapW - 1, mapH - 1);

  const sx = mapW / state.model.grid.width;
  const sy = mapH / state.model.grid.height;
  for (let gy = 0; gy < state.model.grid.height; gy += 1) {
    for (let gx = 0; gx < state.model.grid.width; gx += 1) {
      const cell = state.model.grid.get(gx, gy);
      if (cell === 0) {
        continue;
      }
      ctx.fillStyle = state.model.colorForState(cell);
      const px = x + gx * sx;
      const py = y + gy * sy;
      ctx.fillRect(px, py, Math.max(1, sx), Math.max(1, sy));
    }
  }

  const worldW = state.model.grid.width * state.cellSize;
  const worldH = state.model.grid.height * state.cellSize;
  const vx = x + (state.viewportX / worldW) * mapW;
  const vy = y + (state.viewportY / worldH) * mapH;
  const vw = (canvas.width / worldW) * mapW;
  const vh = (canvas.height / worldH) * mapH;
  ctx.strokeStyle = "#78b7ff";
  ctx.lineWidth = 1.5;
  ctx.strokeRect(vx + 0.5, vy + 0.5, Math.max(2, vw - 1), Math.max(2, vh - 1));
}

function minimapContains(clientX: number, clientY: number): boolean {
  if (!minimap) {
    return false;
  }
  const rect = canvas.getBoundingClientRect();
  const x = clientX - rect.left;
  const y = clientY - rect.top;
  return x >= minimap.x && x <= minimap.x + minimap.w && y >= minimap.y && y <= minimap.y + minimap.h;
}

function jumpViewportFromMinimap(clientX: number, clientY: number): void {
  if (!minimap) {
    return;
  }
  const rect = canvas.getBoundingClientRect();
  const px = clientX - rect.left - minimap.x;
  const py = clientY - rect.top - minimap.y;
  const tx = px / minimap.w;
  const ty = py / minimap.h;

  const worldW = state.model.grid.width * state.cellSize;
  const worldH = state.model.grid.height * state.cellSize;
  state.viewportX = tx * worldW - canvas.width * 0.5;
  state.viewportY = ty * worldH - canvas.height * 0.5;
  clampViewport();
  render();
}

function tick(): void {
  if (!state.running) {
    return;
  }
  state.model.step();
  state.generation += 1;
  render();
}

function restartTimer(): void {
  if (state.timer) {
    window.clearInterval(state.timer);
  }
  const ms = Math.max(16, Math.floor(1000 / state.speed));
  state.timer = window.setInterval(tick, ms);
}

function toCellCoords(ev: PointerEvent): { x: number; y: number } | null {
  const rect = canvas.getBoundingClientRect();
  const x = Math.floor((state.viewportX + ev.clientX - rect.left) / state.cellSize);
  const y = Math.floor((state.viewportY + ev.clientY - rect.top) / state.cellSize);
  if (x < 0 || y < 0 || x >= state.model.grid.width || y >= state.model.grid.height) {
    return null;
  }
  return { x, y };
}

function paintCell(x: number, y: number, button: number): void {
  if (button === 2) {
    state.model.grid.set(x, y, 0);
  } else {
    state.model.handleClick(x, y);
  }
}

fillSelect(modelSelect, ALL_MODELS, state.modelName);
if (restorePersistedState()) {
  fillSelect(modelSelect, ALL_MODELS, state.modelName);
  fillSelect(patternSelect, state.model.patterns, state.pattern);
  speedInput.value = String(state.speed);
  boundarySelect.value = state.boundary;
  cellSizeInput.value = String(Math.round(state.cellSize));
  setStatus("Restored saved session.");
} else {
  rebuildModel();
}
restartTimer();

speedValue.textContent = `${state.speed} /s`;
cellSizeValue.textContent = `${state.cellSize}px`;
updateStats();

modelSelect.addEventListener("change", () => {
  state.modelName = modelSelect.value;
  rebuildModel();
});

patternSelect.addEventListener("change", () => {
  state.pattern = patternSelect.value;
  state.generation = 0;
  state.model.loadPattern(state.pattern);
  render();
  setStatus(`Pattern: ${state.pattern}`);
  persistState();
});

speedInput.addEventListener("input", () => {
  state.speed = Number(speedInput.value);
  speedValue.textContent = `${state.speed} /s`;
  restartTimer();
  persistState();
});

boundarySelect.addEventListener("change", () => {
  state.boundary =
    boundarySelect.value === "fixed"
      ? "fixed"
      : boundarySelect.value === "reflect"
        ? "reflect"
        : "wrap";
  rebuildModel();
});

cellSizeInput.addEventListener("input", () => {
  state.cellSize = Number(cellSizeInput.value);
  cellSizeValue.textContent = `${state.cellSize}px`;
  render();
  persistState();
});

playButton.addEventListener("click", () => {
  state.running = !state.running;
  playButton.textContent = state.running ? "Pause" : "Play";
  setStatus(state.running ? "Simulation running." : "Simulation paused.");
});

stepButton.addEventListener("click", () => {
  pushUndoSnapshot();
  state.model.step();
  state.generation += 1;
  render();
  setStatus("Stepped one generation.");
  persistState();
});

resetButton.addEventListener("click", () => {
  pushUndoSnapshot();
  state.model.reset();
  state.model.loadPattern(state.pattern);
  state.generation = 0;
  render();
  setStatus("Reset to selected pattern.");
  persistState();
});

randomButton.addEventListener("click", () => {
  pushUndoSnapshot();
  state.pattern = state.model.patterns.includes("Random Soup")
    ? "Random Soup"
    : state.model.patterns[0] ?? "Random Soup";
  state.generation = 0;
  state.model.loadPattern(state.pattern);
  fillSelect(patternSelect, state.model.patterns, state.pattern);
  render();
  setStatus(`Pattern: ${state.pattern}`);
  persistState();
});

clearButton.addEventListener("click", () => {
  pushUndoSnapshot();
  state.model.reset();
  state.generation = 0;
  render();
  setStatus("Grid cleared.");
  persistState();
});

undoButton.addEventListener("click", () => {
  applyUndo();
});

redoButton.addEventListener("click", () => {
  applyRedo();
});

exportPngButton.addEventListener("click", () => {
  exportPng();
});

centerViewButton.addEventListener("click", () => {
  centerView();
  setStatus("Centered viewport.");
  persistState();
});

fitViewButton.addEventListener("click", () => {
  fitView();
  setStatus("Fit grid to viewport.");
  persistState();
});

runNButton.addEventListener("click", () => {
  runNSteps(Number.parseInt(runNInput.value, 10));
});

saveStateButton.addEventListener("click", () => {
  persistState();
  setStatus("Saved session.");
});

loadStateButton.addEventListener("click", () => {
  if (!restorePersistedState()) {
    setStatus("No saved session found.");
    return;
  }
  fillSelect(modelSelect, ALL_MODELS, state.modelName);
  fillSelect(patternSelect, state.model.patterns, state.pattern);
  speedInput.value = String(state.speed);
  speedValue.textContent = `${state.speed} /s`;
  boundarySelect.value = state.boundary;
  cellSizeInput.value = String(Math.round(state.cellSize));
  cellSizeValue.textContent = `${Math.round(state.cellSize)}px`;
  playButton.textContent = state.running ? "Pause" : "Play";
  render();
  setStatus("Loaded saved session.");
});

canvas.addEventListener("contextmenu", (ev) => {
  ev.preventDefault();
});

canvas.addEventListener("pointerdown", (ev) => {
  if (ev.button === 0 && minimapContains(ev.clientX, ev.clientY)) {
    jumpViewportFromMinimap(ev.clientX, ev.clientY);
    return;
  }

  if (ev.button === 1) {
    panPointerId = ev.pointerId;
    panStartClientX = ev.clientX;
    panStartClientY = ev.clientY;
    panStartViewportX = state.viewportX;
    panStartViewportY = state.viewportY;
    canvas.setPointerCapture(ev.pointerId);
    return;
  }

  const coords = toCellCoords(ev);
  if (!coords) {
    return;
  }
  if (!dragSnapshotPushed) {
    pushUndoSnapshot();
    dragSnapshotPushed = true;
  }
  dragPointerId = ev.pointerId;
  dragButton = ev.button;
  canvas.setPointerCapture(ev.pointerId);
  paintCell(coords.x, coords.y, ev.button);
  render();
});

canvas.addEventListener("pointermove", (ev) => {
  if (panPointerId === ev.pointerId && minimapContains(ev.clientX, ev.clientY)) {
    jumpViewportFromMinimap(ev.clientX, ev.clientY);
    return;
  }

  if (panPointerId === ev.pointerId) {
    const dx = ev.clientX - panStartClientX;
    const dy = ev.clientY - panStartClientY;
    state.viewportX = panStartViewportX - dx;
    state.viewportY = panStartViewportY - dy;
    render();
    return;
  }

  if (dragPointerId !== ev.pointerId) {
    return;
  }
  if ((ev.buttons & 1) === 0 && (ev.buttons & 2) === 0) {
    return;
  }
  const coords = toCellCoords(ev);
  if (!coords) {
    return;
  }
  const button = (ev.buttons & 2) !== 0 ? 2 : dragButton;
  if (button === 2) {
    state.model.grid.set(coords.x, coords.y, 0);
  } else {
    if (state.model.grid.get(coords.x, coords.y) === 0) {
      state.model.grid.set(coords.x, coords.y, 1);
    }
  }
  render();
});

canvas.addEventListener("pointerup", () => {
  dragPointerId = null;
  dragSnapshotPushed = false;
  panPointerId = null;
});

canvas.addEventListener("pointercancel", () => {
  dragPointerId = null;
  dragSnapshotPushed = false;
  panPointerId = null;
});

canvas.addEventListener("wheel", (ev) => {
  ev.preventDefault();
  const rect = canvas.getBoundingClientRect();
  const mx = ev.clientX - rect.left;
  const my = ev.clientY - rect.top;
  const oldSize = state.cellSize;
  const factor = ev.deltaY < 0 ? 1.1 : 0.9;
  const newSize = Math.max(4, Math.min(24, oldSize * factor));
  const gx = (state.viewportX + mx) / oldSize;
  const gy = (state.viewportY + my) / oldSize;
  state.cellSize = newSize;
  state.viewportX = gx * newSize - mx;
  state.viewportY = gy * newSize - my;
  cellSizeInput.value = String(Math.round(newSize));
  cellSizeValue.textContent = `${Math.round(newSize)}px`;
  render();
});

window.addEventListener("keydown", (ev) => {
  const target = ev.target as HTMLElement | null;
  if (target && (target.tagName === "INPUT" || target.tagName === "SELECT")) {
    return;
  }
  if (ev.code === "Space") {
    ev.preventDefault();
    playButton.click();
  } else if (ev.ctrlKey && ev.key.toLowerCase() === "z") {
    ev.preventDefault();
    applyUndo();
  } else if (ev.ctrlKey && (ev.key.toLowerCase() === "y" || (ev.shiftKey && ev.key.toLowerCase() === "z"))) {
    ev.preventDefault();
    applyRedo();
  } else if (ev.key.toLowerCase() === "s") {
    stepButton.click();
  } else if (ev.key.toLowerCase() === "r") {
    resetButton.click();
  } else if (ev.key.toLowerCase() === "e") {
    exportPng();
  } else if (ev.key.toLowerCase() === "c") {
    centerView();
    setStatus("Centered viewport.");
  } else if (ev.key.toLowerCase() === "f") {
    fitView();
    setStatus("Fit grid to viewport.");
  } else if (ev.key.toLowerCase() === "n") {
    runNSteps(Number.parseInt(runNInput.value, 10));
  } else if (ev.key === "+" || ev.key === "=") {
    state.cellSize = Math.min(24, state.cellSize + 1);
    cellSizeInput.value = String(Math.round(state.cellSize));
    cellSizeValue.textContent = `${Math.round(state.cellSize)}px`;
    render();
    persistState();
  } else if (ev.key === "-") {
    state.cellSize = Math.max(4, state.cellSize - 1);
    cellSizeInput.value = String(Math.round(state.cellSize));
    cellSizeValue.textContent = `${Math.round(state.cellSize)}px`;
    render();
    persistState();
  }
});

window.addEventListener("beforeunload", () => {
  persistState();
});

setStatus("Ready.");
render();
