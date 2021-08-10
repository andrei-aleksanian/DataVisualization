export type Points2D = [number, number, 0];
export type Points3D = [number, number, number];

// Data common
export interface DataCore {
  dimension2D: boolean;
}

// Data IN, uncolored:
export interface Data extends DataCore {
  labels: number[];
}

export interface Data2D extends Data {
  points: Points2D[];
}

export interface Data3D extends Data {
  points: Points3D[];
}

// Data WITHIN React, colored:

export interface DataColored extends DataCore {
  colors: string[];
}

export interface Data2DColored extends DataColored {
  points: Points2D[];
}
export interface Data3DColored extends DataColored {
  points: Points3D[];
}

// Data here is not used atm
export const DATA: Data2D = {
  points: [
    [0, 0, 0],
    [0, 1, 0],
    [0, 2, 0],
    [3, 1, 0],
    [3, 2, 0],
    [3, 1, 0],
    [-3, 4, 0],
    [-3, 1, 0],
  ],
  labels: [1, 1, 1, 0, 0, 0, 3, 3],
  dimension2D: true,
};
