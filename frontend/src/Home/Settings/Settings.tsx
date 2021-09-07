import Slider from 'Components/Forms/Slider';

import { Algorithm } from 'types/Settings';
import CheckBoxes from 'Components/Forms/CheckBoxes';

import { LinkBack } from 'Components/Link';
import classes from './Settings.module.scss';
import COVA, { SettingsCOVA } from './components/COVA';
import ANGEL, { SettingsANGEL } from './components/ANGEL';

export const TEXT_CHECKBOX_COVA = 'COVA';
export const TEXT_CHECKBOX_ANGEL = 'ANGEL';
export const TEXT_H1 = 'Example: Cylinder';
export const TEXT_CHECKBOX_ALGORITHM = 'Algorithm:';
export const TEXT_SLIDER_NEIGHBOUR = 'Neighbour number:';
export const TEXT_SLIDER_LAMBDA = 'Lambda:';
export const TEXT_CHECKBOX_PRESERVATION = 'Show Data Preservation Error:';

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
export const defaultSettingsCommon: SettingsCommon = {
  dataPreservation: DataPreservation.OFF,
  algorithm: Algorithm.COVA,
  neighbour: 0,
  lambda: 0,
};

export const NEIGHBOUR_MARKS_ARR = ['10', '20', '30', '10%', '30%', '50%'];
export interface SettingsProps {
  settingsCommon: SettingsCommon;
  setSettingsCommon: React.Dispatch<React.SetStateAction<SettingsCommon>>;
  settingsCOVA: SettingsCOVA;
  setSettingsCOVA: React.Dispatch<React.SetStateAction<SettingsCOVA>>;
  settingsANGEL: SettingsANGEL;
  setSettingsANGEL: React.Dispatch<React.SetStateAction<SettingsANGEL>>;
  backLink: string;
}

const Settings = ({
  settingsCommon,
  setSettingsCommon,
  settingsCOVA,
  setSettingsCOVA,
  settingsANGEL,
  setSettingsANGEL,
  backLink,
}: SettingsProps) => {
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
      <LinkBack link={backLink} />
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
        max={5}
        step={1}
        marksArr={NEIGHBOUR_MARKS_ARR}
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
