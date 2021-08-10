import { DataLabelled, DataCore } from './Data';

// Data for Preservance demo (demo 2)

export interface DataPerseveranceCore extends DataCore {
  prevPartsave: number[];
  prevWrongInLow: number[][];
  prevWrongInHigh: number[][];
}

/*
  Data with labels.
  Used for getting colors and transforming into Colored data later.
*/
export interface DataPerseverance extends DataLabelled, DataPerseveranceCore {}

export interface DataPerseveranceColored extends DataPerseveranceCore {
  colors: string[];
}

// dummy example data
export const DATA_PERSEVERANCE: DataPerseverance = {
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
  prevPartsave: [],
  prevWrongInHigh: [[]],
  prevWrongInLow: [[]],
};
