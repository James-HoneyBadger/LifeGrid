import { Grid } from "../core/grid";
import type { Automaton, BoundaryMode } from "../core/types";
import { LifeLikeAutomaton } from "./baseLifeLike";

function wrap(n: number, size: number): number {
  return (n + size) % size;
}

function resolveCoord(n: number, size: number, boundary: BoundaryMode): number | null {
  if (boundary === "wrap") {
    return wrap(n, size);
  }
  if (boundary === "fixed") {
    if (n < 0 || n >= size) {
      return null;
    }
    return n;
  }

  if (size <= 1) {
    return 0;
  }

  let v = n;
  while (v < 0 || v >= size) {
    if (v < 0) {
      v = -v - 1;
    } else {
      v = 2 * size - v - 1;
    }
  }
  return v;
}

function countAliveNeighbors(grid: Grid, x: number, y: number, boundary: BoundaryMode): number {
  let count = 0;
  for (let dy = -1; dy <= 1; dy += 1) {
    for (let dx = -1; dx <= 1; dx += 1) {
      if (dx === 0 && dy === 0) {
        continue;
      }
      const nx = resolveCoord(x + dx, grid.width, boundary);
      const ny = resolveCoord(y + dy, grid.height, boundary);
      if (nx === null || ny === null) {
        continue;
      }
      if (grid.get(nx, ny) > 0) {
        count += 1;
      }
    }
  }
  return count;
}

function aliveNeighborStats(grid: Grid, x: number, y: number, boundary: BoundaryMode): { count: number; sum: number } {
  let count = 0;
  let sum = 0;
  for (let dy = -1; dy <= 1; dy += 1) {
    for (let dx = -1; dx <= 1; dx += 1) {
      if (dx === 0 && dy === 0) {
        continue;
      }
      const nx = resolveCoord(x + dx, grid.width, boundary);
      const ny = resolveCoord(y + dy, grid.height, boundary);
      if (nx === null || ny === null) {
        continue;
      }
      const v = grid.get(nx, ny);
      if (v > 0) {
        count += 1;
        sum += v;
      }
    }
  }
  return { count, sum };
}

export class ConwayModel extends LifeLikeAutomaton {
  constructor(width: number, height: number, boundary: BoundaryMode = "wrap") {
    super("Conway", width, height, { birth: [3], survival: [2, 3] }, ["Glider", "Blinker", "Random Soup"], boundary);
  }

  protected override patternPoints(pattern: string): Array<[number, number]> {
    if (pattern === "Glider") {
      return [[0, -1], [1, 0], [-1, 1], [0, 1], [1, 1]];
    }
    if (pattern === "Blinker") {
      return [[-1, 0], [0, 0], [1, 0]];
    }
    return [];
  }
}

export class HighLifeModel extends LifeLikeAutomaton {
  constructor(width: number, height: number, boundary: BoundaryMode = "wrap") {
    super("High Life", width, height, { birth: [3, 6], survival: [2, 3] }, ["Replicator", "Random Soup"], boundary);
  }

  protected override patternPoints(pattern: string): Array<[number, number]> {
    if (pattern === "Replicator") {
      return [[0, -1], [-1, 0], [0, 0], [1, 0], [-1, 1], [1, 1], [0, 2]];
    }
    return [];
  }
}

export class SeedsModel extends LifeLikeAutomaton {
  constructor(width: number, height: number, boundary: BoundaryMode = "wrap") {
    super("Seeds", width, height, { birth: [2], survival: [] }, ["Twin Pairs", "Random Soup"], boundary);
  }

  protected override patternPoints(pattern: string): Array<[number, number]> {
    if (pattern === "Twin Pairs") {
      return [[-2, 0], [-1, 0], [1, 0], [2, 0], [0, 2], [0, -2]];
    }
    return [];
  }
}

export class DayNightModel extends LifeLikeAutomaton {
  constructor(width: number, height: number, boundary: BoundaryMode = "wrap") {
    super("Day & Night", width, height, { birth: [3, 6, 7, 8], survival: [3, 4, 6, 7, 8] }, ["Diamond", "Random Soup"], boundary);
  }

  protected override patternPoints(pattern: string): Array<[number, number]> {
    if (pattern === "Diamond") {
      return [[0, -2], [-1, -1], [1, -1], [-2, 0], [2, 0], [-1, 1], [1, 1], [0, 2]];
    }
    return [];
  }
}

export class MazeModel extends LifeLikeAutomaton {
  constructor(width: number, height: number, boundary: BoundaryMode = "wrap") {
    super("Maze", width, height, { birth: [3], survival: [1, 2, 3, 4, 5] }, ["Core", "Random Soup"], boundary);
  }

  protected override patternPoints(pattern: string): Array<[number, number]> {
    if (pattern === "Core") {
      return [[-2, -2], [-1, -2], [0, -2], [1, -2], [2, -2], [-2, -1], [2, -1], [-2, 0], [0, 0], [2, 0], [-2, 1], [2, 1], [-2, 2], [-1, 2], [0, 2], [1, 2], [2, 2]];
    }
    return [];
  }
}

export class BriansBrainModel implements Automaton {
  readonly name = "Brian's Brain";
  readonly patterns = ["Random Soup"];
  grid: Grid;
  private readonly boundary: BoundaryMode;

  constructor(width: number, height: number, boundary: BoundaryMode = "wrap") {
    this.grid = new Grid(width, height);
    this.boundary = boundary;
  }

  step(): void {
    const next = new Uint8Array(this.grid.cells.length);
    for (let y = 0; y < this.grid.height; y += 1) {
      for (let x = 0; x < this.grid.width; x += 1) {
        const i = this.grid.idx(x, y);
        const v = this.grid.cells[i];
        const firing = (() => {
          let c = 0;
          for (let dy = -1; dy <= 1; dy += 1) {
            for (let dx = -1; dx <= 1; dx += 1) {
              if (dx === 0 && dy === 0) {
                continue;
              }
              const nx = resolveCoord(x + dx, this.grid.width, this.boundary);
              const ny = resolveCoord(y + dy, this.grid.height, this.boundary);
              if (nx === null || ny === null) {
                continue;
              }
              if (this.grid.get(nx, ny) === 1) {
                c += 1;
              }
            }
          }
          return c;
        })();

        next[i] = v === 0 ? Number(firing === 2) : v === 1 ? 2 : 0;
      }
    }
    this.grid.cells = next;
  }

  reset(): void {
    this.grid.clear();
  }

  loadPattern(_pattern: string): void {
    this.grid.clear();
    for (let i = 0; i < this.grid.cells.length; i += 1) {
      this.grid.cells[i] = Math.random() < 0.08 ? 1 : 0;
    }
  }

  handleClick(x: number, y: number): void {
    const v = this.grid.get(x, y);
    this.grid.set(x, y, v === 0 ? 1 : 0);
  }

  colorForState(state: number): string {
    if (state === 1) {
      return "#58a6ff";
    }
    if (state === 2) {
      return "#7f8c9f";
    }
    return "#0f1115";
  }
}

export class WireworldModel implements Automaton {
  readonly name = "Wireworld";
  readonly patterns = ["Random Soup"];
  grid: Grid;
  private readonly boundary: BoundaryMode;

  constructor(width: number, height: number, boundary: BoundaryMode = "wrap") {
    this.grid = new Grid(width, height);
    this.boundary = boundary;
  }

  step(): void {
    const next = new Uint8Array(this.grid.cells.length);
    for (let y = 0; y < this.grid.height; y += 1) {
      for (let x = 0; x < this.grid.width; x += 1) {
        const i = this.grid.idx(x, y);
        const v = this.grid.cells[i];
        if (v === 0) {
          next[i] = 0;
        } else if (v === 1) {
          next[i] = 2;
        } else if (v === 2) {
          next[i] = 3;
        } else {
          let heads = 0;
          for (let dy = -1; dy <= 1; dy += 1) {
            for (let dx = -1; dx <= 1; dx += 1) {
              if (dx === 0 && dy === 0) {
                continue;
              }
              const nx = resolveCoord(x + dx, this.grid.width, this.boundary);
              const ny = resolveCoord(y + dy, this.grid.height, this.boundary);
              if (nx === null || ny === null) {
                continue;
              }
              if (this.grid.get(nx, ny) === 1) {
                heads += 1;
              }
            }
          }
          next[i] = heads === 1 || heads === 2 ? 1 : 3;
        }
      }
    }
    this.grid.cells = next;
  }

  reset(): void {
    this.grid.clear();
  }

  loadPattern(_pattern: string): void {
    this.grid.clear();
    for (let i = 0; i < this.grid.cells.length; i += 1) {
      const r = Math.random();
      this.grid.cells[i] = r < 0.02 ? 1 : r < 0.12 ? 3 : 0;
    }
  }

  handleClick(x: number, y: number): void {
    const v = this.grid.get(x, y);
    this.grid.set(x, y, (v + 1) % 4);
  }

  colorForState(state: number): string {
    if (state === 1) {
      return "#4fc3f7";
    }
    if (state === 2) {
      return "#ef5350";
    }
    if (state === 3) {
      return "#ffd54f";
    }
    return "#0f1115";
  }
}

export class ImmigrationModel implements Automaton {
  readonly name = "Immigration";
  readonly patterns = ["Color Mix", "Random Soup"];
  grid: Grid;
  private readonly boundary: BoundaryMode;

  constructor(width: number, height: number, boundary: BoundaryMode = "wrap") {
    this.grid = new Grid(width, height);
    this.boundary = boundary;
  }

  step(): void {
    const next = new Uint8Array(this.grid.cells.length);
    for (let y = 0; y < this.grid.height; y += 1) {
      for (let x = 0; x < this.grid.width; x += 1) {
        const i = this.grid.idx(x, y);
        const v = this.grid.cells[i];
        const { count, sum } = aliveNeighborStats(this.grid, x, y, this.boundary);
        if (v > 0) {
          next[i] = count === 2 || count === 3 ? v : 0;
        } else if (count === 3) {
          next[i] = (sum % 3) + 1;
        } else {
          next[i] = 0;
        }
      }
    }
    this.grid.cells = next;
  }

  reset(): void {
    this.grid.clear();
  }

  loadPattern(pattern: string): void {
    this.grid.clear();
    if (pattern === "Color Mix") {
      const cx = Math.floor(this.grid.width / 2);
      const cy = Math.floor(this.grid.height / 2);
      const p1: Array<[number, number]> = [[-20, -15], [-19, -15], [-18, -15], [-19, -14], [-18, -13]];
      const p2: Array<[number, number]> = [[0, -15], [1, -15], [2, -15]];
      for (const [dx, dy] of p1) {
        const x = cx + dx;
        const y = cy + dy;
        if (x >= 0 && y >= 0 && x < this.grid.width && y < this.grid.height) {
          this.grid.set(x, y, 1);
        }
      }
      for (const [dx, dy] of p2) {
        const x = cx + dx;
        const y = cy + dy;
        if (x >= 0 && y >= 0 && x < this.grid.width && y < this.grid.height) {
          this.grid.set(x, y, 2);
        }
      }
      return;
    }

    for (let i = 0; i < this.grid.cells.length; i += 1) {
      if (Math.random() < 0.15) {
        this.grid.cells[i] = 1 + Math.floor(Math.random() * 3);
      }
    }
  }

  handleClick(x: number, y: number): void {
    const v = this.grid.get(x, y);
    this.grid.set(x, y, (v + 1) % 4);
  }

  colorForState(state: number): string {
    if (state === 1) {
      return "#ff8a65";
    }
    if (state === 2) {
      return "#4db6ac";
    }
    if (state === 3) {
      return "#ba68c8";
    }
    return "#0f1115";
  }
}

export class RainbowModel implements Automaton {
  readonly name = "Rainbow";
  readonly patterns = ["Rainbow Mix", "Random Soup"];
  grid: Grid;
  private readonly boundary: BoundaryMode;

  constructor(width: number, height: number, boundary: BoundaryMode = "wrap") {
    this.grid = new Grid(width, height);
    this.boundary = boundary;
  }

  step(): void {
    const next = new Uint8Array(this.grid.cells.length);
    for (let y = 0; y < this.grid.height; y += 1) {
      for (let x = 0; x < this.grid.width; x += 1) {
        const i = this.grid.idx(x, y);
        const v = this.grid.cells[i];
        const { count, sum } = aliveNeighborStats(this.grid, x, y, this.boundary);
        if (v > 0) {
          next[i] = count === 2 || count === 3 ? v : 0;
        } else if (count === 3) {
          next[i] = Math.max(1, Math.min(6, Math.floor(sum / 3)));
        } else {
          next[i] = 0;
        }
      }
    }
    this.grid.cells = next;
  }

  reset(): void {
    this.grid.clear();
  }

  loadPattern(_pattern: string): void {
    this.grid.clear();
    for (let i = 0; i < this.grid.cells.length; i += 1) {
      if (Math.random() < 0.15) {
        this.grid.cells[i] = 1 + Math.floor(Math.random() * 6);
      }
    }
  }

  handleClick(x: number, y: number): void {
    const v = this.grid.get(x, y);
    this.grid.set(x, y, (v + 1) % 7);
  }

  colorForState(state: number): string {
    const colors = ["#0f1115", "#ef5350", "#ff9800", "#ffee58", "#66bb6a", "#42a5f5", "#ab47bc"];
    return colors[state] ?? "#0f1115";
  }
}

export class HexagonalModel implements Automaton {
  readonly name = "Hexagonal";
  readonly patterns = ["Random Soup"];
  grid: Grid;
  private readonly boundary: BoundaryMode;

  constructor(width: number, height: number, boundary: BoundaryMode = "wrap") {
    this.grid = new Grid(width, height);
    this.boundary = boundary;
  }

  private hexNeighbors(x: number, y: number): number {
    const even = [[-1, 0], [1, 0], [-1, -1], [0, -1], [-1, 1], [0, 1]];
    const odd = [[-1, 0], [1, 0], [0, -1], [1, -1], [0, 1], [1, 1]];
    const offsets = y % 2 === 0 ? even : odd;
    let count = 0;
    for (const [dx, dy] of offsets) {
      const nx = resolveCoord(x + dx, this.grid.width, this.boundary);
      const ny = resolveCoord(y + dy, this.grid.height, this.boundary);
      if (nx === null || ny === null) {
        continue;
      }
      if (this.grid.get(nx, ny) > 0) {
        count += 1;
      }
    }
    return count;
  }

  step(): void {
    const next = new Uint8Array(this.grid.cells.length);
    for (let y = 0; y < this.grid.height; y += 1) {
      for (let x = 0; x < this.grid.width; x += 1) {
        const i = this.grid.idx(x, y);
        const alive = this.grid.cells[i] > 0;
        const n = this.hexNeighbors(x, y);
        next[i] = alive ? Number(n === 3 || n === 4) : Number(n === 2);
      }
    }
    this.grid.cells = next;
  }

  reset(): void {
    this.grid.clear();
  }

  loadPattern(_pattern: string): void {
    this.grid.clear();
    for (let i = 0; i < this.grid.cells.length; i += 1) {
      this.grid.cells[i] = Math.random() < 0.15 ? 1 : 0;
    }
  }

  handleClick(x: number, y: number): void {
    const v = this.grid.get(x, y);
    this.grid.set(x, y, v === 0 ? 1 : 0);
  }

  colorForState(state: number): string {
    return state === 0 ? "#0f1115" : "#d0f0ff";
  }
}

export class GenerationsModel implements Automaton {
  readonly name = "Generations";
  readonly patterns = ["Random Soup"];
  grid: Grid;
  private readonly nStates = 8;
  private readonly boundary: BoundaryMode;

  constructor(width: number, height: number, boundary: BoundaryMode = "wrap") {
    this.grid = new Grid(width, height);
    this.boundary = boundary;
  }

  step(): void {
    const next = new Uint8Array(this.grid.cells.length);
    for (let y = 0; y < this.grid.height; y += 1) {
      for (let x = 0; x < this.grid.width; x += 1) {
        const i = this.grid.idx(x, y);
        const s = this.grid.cells[i];
        let aliveNeighbors = 0;
        for (let dy = -1; dy <= 1; dy += 1) {
          for (let dx = -1; dx <= 1; dx += 1) {
            if (dx === 0 && dy === 0) {
              continue;
            }
            const nx = resolveCoord(x + dx, this.grid.width, this.boundary);
            const ny = resolveCoord(y + dy, this.grid.height, this.boundary);
            if (nx === null || ny === null) {
              continue;
            }
            if (this.grid.get(nx, ny) === 1) {
              aliveNeighbors += 1;
            }
          }
        }

        if (s === 0) {
          next[i] = aliveNeighbors === 3 ? 1 : 0;
        } else if (s === 1) {
          next[i] = aliveNeighbors === 2 || aliveNeighbors === 3 ? 1 : 2;
        } else if (s < this.nStates - 1) {
          next[i] = s + 1;
        } else {
          next[i] = 0;
        }
      }
    }
    this.grid.cells = next;
  }

  reset(): void {
    this.grid.clear();
  }

  loadPattern(_pattern: string): void {
    this.grid.clear();
    for (let i = 0; i < this.grid.cells.length; i += 1) {
      this.grid.cells[i] = Math.random() < 0.15 ? 1 : 0;
    }
  }

  handleClick(x: number, y: number): void {
    const v = this.grid.get(x, y);
    this.grid.set(x, y, (v + 1) % this.nStates);
  }

  colorForState(state: number): string {
    const colors = ["#0f1115", "#ffffff", "#ff8a65", "#ffb74d", "#fff176", "#81c784", "#64b5f6", "#9575cd"];
    return colors[state] ?? "#0f1115";
  }
}

export class LangtonsAntModel implements Automaton {
  readonly name = "Langton's Ant";
  readonly patterns = ["Empty"];
  grid: Grid;
  private base: Uint8Array;
  private antX: number;
  private antY: number;
  private antDir: number;
  private readonly boundary: BoundaryMode;

  constructor(width: number, height: number, boundary: BoundaryMode = "wrap") {
    this.grid = new Grid(width, height);
    this.base = new Uint8Array(width * height);
    this.antX = Math.floor(width / 2);
    this.antY = Math.floor(height / 2);
    this.antDir = 0;
    this.boundary = boundary;
    this.syncAntMarker();
  }

  private syncAntMarker(): void {
    this.grid.cells.set(this.base);
    this.grid.cells[this.grid.idx(this.antX, this.antY)] = 2;
  }

  step(): void {
    const i = this.grid.idx(this.antX, this.antY);
    const current = this.base[i];
    this.base[i] = current === 0 ? 1 : 0;

    this.antDir = current === 0 ? (this.antDir + 1) % 4 : (this.antDir + 3) % 4;

    const moveAnt = (nextX: number, nextY: number): void => {
      const resolvedX = resolveCoord(nextX, this.grid.width, this.boundary);
      const resolvedY = resolveCoord(nextY, this.grid.height, this.boundary);
      if (resolvedX === null || resolvedY === null) {
        return;
      }
      this.antX = resolvedX;
      this.antY = resolvedY;
    };

    if (this.antDir === 0) {
      moveAnt(this.antX, this.antY - 1);
    } else if (this.antDir === 1) {
      moveAnt(this.antX + 1, this.antY);
    } else if (this.antDir === 2) {
      moveAnt(this.antX, this.antY + 1);
    } else {
      moveAnt(this.antX - 1, this.antY);
    }

    this.syncAntMarker();
  }

  reset(): void {
    this.base.fill(0);
    this.antX = Math.floor(this.grid.width / 2);
    this.antY = Math.floor(this.grid.height / 2);
    this.antDir = 0;
    this.syncAntMarker();
  }

  loadPattern(_pattern: string): void {
    this.reset();
  }

  handleClick(x: number, y: number): void {
    this.antX = x;
    this.antY = y;
    this.syncAntMarker();
  }

  colorForState(state: number): string {
    if (state === 1) {
      return "#e6f2ff";
    }
    if (state === 2) {
      return "#ff7043";
    }
    return "#0f1115";
  }
}

export function createModel(
  mode: string,
  width: number,
  height: number,
  boundary: BoundaryMode = "wrap",
): Automaton {
  switch (mode) {
    case "Conway":
      return new ConwayModel(width, height, boundary);
    case "High Life":
      return new HighLifeModel(width, height, boundary);
    case "Seeds":
      return new SeedsModel(width, height, boundary);
    case "Day & Night":
      return new DayNightModel(width, height, boundary);
    case "Maze":
      return new MazeModel(width, height, boundary);
    case "Wireworld":
      return new WireworldModel(width, height, boundary);
    case "Brian's Brain":
      return new BriansBrainModel(width, height, boundary);
    case "Immigration":
      return new ImmigrationModel(width, height, boundary);
    case "Rainbow":
      return new RainbowModel(width, height, boundary);
    case "Hexagonal":
      return new HexagonalModel(width, height, boundary);
    case "Generations":
      return new GenerationsModel(width, height, boundary);
    case "Langton's Ant":
      return new LangtonsAntModel(width, height, boundary);
    default:
      return new ConwayModel(width, height, boundary);
  }
}

export const ALL_MODELS = [
  "Conway",
  "High Life",
  "Seeds",
  "Day & Night",
  "Maze",
  "Wireworld",
  "Brian's Brain",
  "Immigration",
  "Rainbow",
  "Hexagonal",
  "Generations",
  "Langton's Ant",
];
