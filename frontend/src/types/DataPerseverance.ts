import { DataColored, Points2D, Points3D } from './Data';

// Data for Preservance demo (demo 2)
export interface DataPerseverance extends DataColored {
  prevPartsave: number[];
  prevWrongInLow: number[][];
  prevWrongInHigh: number[][];
}

export interface DataPerseverance2D extends DataPerseverance {
  points: Points2D[];
}
export interface DataPerseverance3D extends DataPerseverance {
  points: Points3D[];
}
