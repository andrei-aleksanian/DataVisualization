export enum Algorithm {
  COVA,
  ANGEL,
  COVA_PERSEVERANCE,
}

export interface SettingsInterface {
  algorithm: Algorithm;
}

export const defaultSettings: SettingsInterface = {
  algorithm: Algorithm.COVA,
};
