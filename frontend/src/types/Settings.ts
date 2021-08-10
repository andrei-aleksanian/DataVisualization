export enum Algorithm {
  COVA,
  ANGEL,
  COVA_PESEVERANCE,
}

export interface SettingsInterface {
  algorithm: Algorithm;
}

export const defaultSettings: SettingsInterface = {
  algorithm: Algorithm.COVA,
};
