export type Points2D = [number, number, 0];

export type Points3D = [number, number, number];

export interface Data {
  labels: number[];
}
export interface Data2D extends Data {
  points: Points2D[];
}

export interface Data3D extends Data {
  points: Points3D[];
}

// Data here is not used atm
export const DATA: Data2D = {
  points: [
    [0, 0, 0],
    [1, 10, 0],
    [0, 9, 0],
    [1, 1, 0],
    [0, 2, 0],
    [1, 1, 0],
    [0, 4, 0],
    [1, 1, 0],
  ],
  labels: [1, 1, 1, 0, 0, 0, 3, 3],
};
