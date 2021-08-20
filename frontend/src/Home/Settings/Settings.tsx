import Slider from 'Components/Forms/Slider';
import { useState } from 'react';
import { LinkBack } from 'Components/Link';

import { Algorithm } from 'types/Settings';
import CheckBoxes from 'Components/Forms/CheckBoxes';

import classes from './Settings.module.scss';
import COVA, { defaultSettingsCOVA } from './components/COVA';
import ANGEL, { defaultSettingsANGEL } from './components/ANGEL';

export const H1_TEXT = 'Example: Cylinder';

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
      <h1>{H1_TEXT}</h1>
      <CheckBoxes
        heading="Algorithm:"
        currentValue={settingsCommon.algorithm}
        onChange={onChangeAlgorithm}
        entries={[
          { value: Algorithm.COVA, text: 'COVA' },
          { value: Algorithm.ANGEL, text: 'ANGEL' },
        ]}
      />
      <Slider
        min={0}
        max={7}
        step={1}
        marksArr={['10', '20', '30', '10%', '20%', '30%', '40%', '50%']}
        onChange={onChangeNeighbour}
        text="Neighbour"
        value={settingsCommon.neighbour}
      />
      <Slider
        min={0}
        max={1}
        step={0.2}
        marksArr={[0, 0.2, 0.4, 0.6, 0.8, 1]}
        onChange={onChangeLambda}
        text="Lambda"
        value={settingsCommon.lambda}
      />
      {settingsCommon.algorithm === Algorithm.COVA ? (
        <COVA {...{ settingsCOVA, setSettingsCOVA }} />
      ) : (
        <ANGEL {...{ settingsANGEL, setSettingsANGEL }} />
      )}
      <CheckBoxes
        heading="Show Data Preservation"
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
