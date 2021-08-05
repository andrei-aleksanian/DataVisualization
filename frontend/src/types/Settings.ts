export enum Algorithm {
  COVA,
  ANGEL,
}

export interface SettingsInterface {
  algorithm: Algorithm;
}

export const defaultSettings: SettingsInterface = {
  algorithm: Algorithm.COVA,
};
