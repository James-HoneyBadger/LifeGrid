import { Grid } from "./grid";

export type BoundaryMode = "wrap" | "fixed" | "reflect";

export interface Automaton {
  readonly name: string;
  readonly patterns: string[];
  grid: Grid;
  step(): void;
  reset(): void;
  loadPattern(pattern: string): void;
  handleClick(x: number, y: number): void;
  colorForState(state: number): string;
}

export interface LifeLikeRule {
  birth: number[];
  survival: number[];
}
