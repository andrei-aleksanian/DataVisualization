export type Points2D = [number, number, 0];

export type Points3D = [number, number, number];

export interface Data2D {
  points: Points2D[];
}

export interface Data3D {
  points: Points3D[];
}

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
};
// Add zeros row to numpy array on the backend !!
