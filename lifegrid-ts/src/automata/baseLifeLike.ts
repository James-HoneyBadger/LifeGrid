import { Grid } from "../core/grid";
import type { Automaton, BoundaryMode, LifeLikeRule } from "../core/types";

function countNeighbors(grid: Grid, x: number, y: number, boundary: BoundaryMode): number {
  const resolveCoord = (n: number, size: number): number | null => {
    if (boundary === "wrap") {
      return (n + size) % size;
    }
    if (boundary === "fixed") {
      return n < 0 || n >= size ? null : n;
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
  };

  let count = 0;
  for (let dy = -1; dy <= 1; dy += 1) {
    for (let dx = -1; dx <= 1; dx += 1) {
      if (dx === 0 && dy === 0) {
        continue;
      }

      const nx = resolveCoord(x + dx, grid.width);
      const ny = resolveCoord(y + dy, grid.height);
      if (nx === null || ny === null) {
        continue;
      }

      if (grid.get(nx, ny) === 1) {
        count += 1;
      }
    }
  }
  return count;
}

export class LifeLikeAutomaton implements Automaton {
  readonly name: string;
  readonly patterns: string[];
  grid: Grid;
  protected readonly rule: LifeLikeRule;
  protected readonly boundary: BoundaryMode;

  constructor(
    name: string,
    width: number,
    height: number,
    rule: LifeLikeRule,
    patterns: string[],
    boundary: BoundaryMode = "wrap",
  ) {
    this.name = name;
    this.grid = new Grid(width, height);
    this.rule = rule;
    this.patterns = patterns;
    this.boundary = boundary;
  }

  step(): void {
    const old = this.grid.cells;
    const next = new Uint8Array(old.length);

    for (let y = 0; y < this.grid.height; y += 1) {
      for (let x = 0; x < this.grid.width; x += 1) {
        const i = this.grid.idx(x, y);
        const alive = old[i] === 1;
        const neighbors = countNeighbors(this.grid, x, y, this.boundary);
        next[i] = alive
          ? Number(this.rule.survival.includes(neighbors))
          : Number(this.rule.birth.includes(neighbors));
      }
    }

    this.grid.cells = next;
  }

  reset(): void {
    this.grid.clear();
  }

  handleClick(x: number, y: number): void {
    const current = this.grid.get(x, y);
    this.grid.set(x, y, current === 0 ? 1 : 0);
  }

  colorForState(state: number): string {
    return state === 0 ? "#0f1115" : "#d0f0ff";
  }

  loadPattern(pattern: string): void {
    this.grid.clear();
    if (pattern === "Random Soup") {
      for (let i = 0; i < this.grid.cells.length; i += 1) {
        this.grid.cells[i] = Math.random() < 0.16 ? 1 : 0;
      }
      return;
    }

    const cx = Math.floor(this.grid.width / 2);
    const cy = Math.floor(this.grid.height / 2);

    const points = this.patternPoints(pattern);
    for (const [dx, dy] of points) {
      const x = cx + dx;
      const y = cy + dy;
      if (x >= 0 && y >= 0 && x < this.grid.width && y < this.grid.height) {
        this.grid.set(x, y, 1);
      }
    }
  }

  protected patternPoints(_pattern: string): Array<[number, number]> {
    return [];
  }
}
