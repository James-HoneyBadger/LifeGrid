import { describe, expect, it } from "vitest";

import { ConwayModel, LangtonsAntModel } from "./models";

describe("boundary behavior", () => {
  it("wrap births a corner cell while fixed and reflect do not", () => {
    const wrapModel = new ConwayModel(5, 5, "wrap");
    const fixedModel = new ConwayModel(5, 5, "fixed");
    const reflectModel = new ConwayModel(5, 5, "reflect");

    const seed = (m: ConwayModel): void => {
      m.reset();
      m.grid.set(4, 4, 1);
      m.grid.set(4, 0, 1);
      m.grid.set(0, 4, 1);
    };

    seed(wrapModel);
    seed(fixedModel);
    seed(reflectModel);

    wrapModel.step();
    fixedModel.step();
    reflectModel.step();

    expect(wrapModel.grid.get(0, 0)).toBe(1);
    expect(fixedModel.grid.get(0, 0)).toBe(0);
    expect(reflectModel.grid.get(0, 0)).toBe(0);
  });

  it("langtons ant respects wrap/fixed/reflect at the top edge", () => {
    const wrapAnt = new LangtonsAntModel(5, 5, "wrap");
    const fixedAnt = new LangtonsAntModel(5, 5, "fixed");
    const reflectAnt = new LangtonsAntModel(5, 5, "reflect");

    const positionAtTopFacingWest = (ant: LangtonsAntModel): void => {
      ant.reset();
      (ant as any).antX = 2;
      (ant as any).antY = 0;
      (ant as any).antDir = 3;
      (ant as any).base.fill(0);
      (ant as any).syncAntMarker();
    };

    positionAtTopFacingWest(wrapAnt);
    positionAtTopFacingWest(fixedAnt);
    positionAtTopFacingWest(reflectAnt);

    wrapAnt.step();
    fixedAnt.step();
    reflectAnt.step();

    expect(((wrapAnt as any).antX)).toBe(2);
    expect(((wrapAnt as any).antY)).toBe(4);

    expect(((fixedAnt as any).antX)).toBe(2);
    expect(((fixedAnt as any).antY)).toBe(0);

    expect(((reflectAnt as any).antX)).toBe(2);
    expect(((reflectAnt as any).antY)).toBe(0);
  });
});
