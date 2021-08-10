export type Point2D = [number, number, 0];
export type Point3D = [number, number, number];
export type Points = Point2D[] | Point3D[];

// Data common properties
export interface DataCore {
  dimension2D: boolean;
  points: Points;
}

// Data IN, with labels and without colors:
export interface DataLabelled extends DataCore {
  labels: number[];
}

// dummy example data
export const DATA: DataLabelled = {
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

// Data colored without labels
export interface DataColored extends DataCore {
  colors: string[];
}
