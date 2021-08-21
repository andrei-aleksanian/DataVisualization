import Slider from 'Components/Forms/Slider';
import { useState } from 'react';
import { LinkBack } from 'Components/Link';

import { Algorithm } from 'types/Settings';
import CheckBoxes from 'Components/Forms/CheckBoxes';

import classes from './Settings.module.scss';
import COVA, { defaultSettingsCOVA } from './components/COVA';
import ANGEL, { defaultSettingsANGEL } from './components/ANGEL';

export const TEXT_CHECKBOX_COVA = 'COVA';
export const TEXT_CHECKBOX_ANGEL = 'ANGEL';
export const TEXT_H1 = 'Example: Cylinder';
export const TEXT_CHECKBOX_ALGORITHM = 'Algorithm:';
export const TEXT_SLIDER_NEIGHBOUR = 'Neighbour:';
export const TEXT_SLIDER_LAMBDA = 'Lambda:';
export const TEXT_CHECKBOX_PRESERVATION = 'Show Data Preservation:';

export enum DataPreservation {
  ON,
  OFF,
}
export interface SettingsCommon {
  dataPreservation: DataPreservation;
  algorithm: Algorithm;
  neighbour: number;
  lambda: number;
}
export const defaultSettingsCommon = {
  dataPreservation: DataPreservation.OFF,
  algorithm: Algorithm.COVA,
  neighbour: 0,
  lambda: 0,
};

const Settings = () => {
  const [settingsCommon, setSettingsCommon] = useState(defaultSettingsCommon);
  const [settingsCOVA, setSettingsCOVA] = useState(defaultSettingsCOVA);
  const [settingsANGEL, setSettingsANGEL] = useState(defaultSettingsANGEL);

  const onChangeAlgorithm = (event: React.ChangeEvent, newAlgorithm: Algorithm) => {
    event.preventDefault();
    setSettingsCommon((prev) => ({ ...prev, algorithm: newAlgorithm }));
  };
  const onChangeNeighbour = (value: number) => setSettingsCommon((prev) => ({ ...prev, neighbour: value }));
  const onChangeLambda = (value: number) => setSettingsCommon((prev) => ({ ...prev, lambda: value }));
  const onChangeDataPreservation = (event: React.ChangeEvent, value: DataPreservation) => {
    event.preventDefault();
    setSettingsCommon((prev) => ({ ...prev, dataPreservation: value }));
  };

  return (
    <div className={classes.index}>
      <LinkBack link="/" />
      <h1>{TEXT_H1}</h1>
      <CheckBoxes
        heading={TEXT_CHECKBOX_ALGORITHM}
        currentValue={settingsCommon.algorithm}
        onChange={onChangeAlgorithm}
        entries={[
          { value: Algorithm.COVA, text: TEXT_CHECKBOX_COVA },
          { value: Algorithm.ANGEL, text: TEXT_CHECKBOX_ANGEL },
        ]}
      />
      <Slider
        min={0}
        max={7}
        step={1}
        marksArr={['10', '20', '30', '10%', '20%', '30%', '40%', '50%']}
        onChange={onChangeNeighbour}
        text={TEXT_SLIDER_NEIGHBOUR}
        value={settingsCommon.neighbour}
      />
      <Slider
        min={0}
        max={1}
        step={0.2}
        marksArr={[0, 0.2, 0.4, 0.6, 0.8, 1]}
        onChange={onChangeLambda}
        text={TEXT_SLIDER_LAMBDA}
        value={settingsCommon.lambda}
      />
      {settingsCommon.algorithm === Algorithm.COVA ? (
        <COVA {...{ settingsCOVA, setSettingsCOVA }} />
      ) : (
        <ANGEL {...{ settingsANGEL, setSettingsANGEL }} />
      )}
      <CheckBoxes
        heading={TEXT_CHECKBOX_PRESERVATION}
        currentValue={settingsCommon.dataPreservation}
        onChange={onChangeDataPreservation}
        entries={[
          { value: DataPreservation.ON, text: 'Yes' },
          { value: DataPreservation.OFF, text: 'No' },
        ]}
      />
    </div>
  );
};

export default Settings;
