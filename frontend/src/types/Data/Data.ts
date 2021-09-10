export type Point2D = [number, number, 0];
export type Point3D = [number, number, number];
export type Points = Point2D[] | Point3D[];

// Data common properties

export interface DataCore {
  dimension2D: boolean;
  iteration: number;
  maxIteration: number;
  g: number[][];
  labels: number[];
  Relation: number[][];
  Ad: number[][];
  V: number[][];
  points: Points;
  alpha: number;
}

// Data IN, with labels and without colors:
export interface DataLabelled extends DataCore {}

// dummy example data
export const DATA: DataLabelled = {
  dimension2D: true,
  // todo: double check
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
  g: [[]],
  labels: [1, 1, 1, 0, 0, 0, 3, 3],
  Relation: [[]],
  Ad: [[]],
  V: [[]],
  alpha: 0.5,
  iteration: 0,
  maxIteration: 0,
};

// Data colored without labels
export interface DataColored extends DataLabelled {
  colors: string[];
}
