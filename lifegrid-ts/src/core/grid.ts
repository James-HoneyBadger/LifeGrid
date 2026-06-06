export class Grid {
  readonly width: number;
  readonly height: number;
  cells: Uint8Array;

  constructor(width: number, height: number) {
    this.width = width;
    this.height = height;
    this.cells = new Uint8Array(width * height);
  }

  clone(): Grid {
    const copy = new Grid(this.width, this.height);
    copy.cells.set(this.cells);
    return copy;
  }

  idx(x: number, y: number): number {
    return y * this.width + x;
  }

  get(x: number, y: number): number {
    return this.cells[this.idx(x, y)];
  }

  set(x: number, y: number, value: number): void {
    this.cells[this.idx(x, y)] = value;
  }

  clear(): void {
    this.cells.fill(0);
  }

  population(): number {
    let pop = 0;
    for (let i = 0; i < this.cells.length; i += 1) {
      if (this.cells[i] !== 0) {
        pop += 1;
      }
    }
    return pop;
  }
}
