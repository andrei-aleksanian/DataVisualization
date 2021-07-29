export type Points2D = {
  x: number;
  y: number;
  z: 0;
}[];

export type Points3D = {
  x: number;
  y: number;
  z: number;
}[];

export interface Data2D {
  points: Points2D;
}

export interface Data3D {
  points: Points3D;
}

export const DATA: Data2D = {
  points: [
    {
      x: 0,
      y: 0,
      z: 0,
    },
    {
      x: 1,
      y: 0,
      z: 0,
    },
    {
      x: 0,
      y: 1,
      z: 0,
    },
    {
      x: 1,
      y: 1,
      z: 0,
    },
  ],
};
