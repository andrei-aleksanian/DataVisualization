export interface Params {
  neighbourNumber: string;
}

export interface ParamsCOVA extends Params {
  alpha: number;
  isCohortNumberOriginal: boolean;
}

export interface ParamsANGEL extends Params {
  anchorDensity: number;
  epsilon: number;
  isAnchorModification: boolean;
}
