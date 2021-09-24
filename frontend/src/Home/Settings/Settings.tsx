import { useState, useEffect, useRef } from 'react';

import { Algorithm } from 'types/Settings';

import CheckBoxes from 'Components/Forms/CheckBoxes';
import Slider from 'Components/Forms/Slider';
import { LinkBack } from 'Components/Link';
import Loader from 'Components/UI/Loader';

import { ModalWithFit } from 'Components/UI';
import COVA, { SettingsCOVA } from './components/COVA';
import ANGEL, { SettingsANGEL } from './components/ANGEL';
import Custom, { CustomProps } from './components/Custom';

import classes from './Settings.module.scss';

export const TEXT_CHECKBOX_COVA = 'COVA';
export const TEXT_CHECKBOX_ANGEL = 'ANGEL';
export const TEXT_CHECKBOX_ORIGINAL = 'See the original data';
export const TEXT_CHECKBOX_ALGORITHM = 'Algorithm:';
export const TEXT_SLIDER_NEIGHBOUR = 'Neighbour number:';
export const TEXT_CHECKBOX_PRESERVATION = 'Show Data Preservation Error:';

export enum DataPreservation {
  ON,
  OFF,
}
export interface SettingsCommon {
  dataPreservation: DataPreservation;
  algorithm: Algorithm;
  neighbour: number;
}
export const defaultSettingsCommon: SettingsCommon = {
  dataPreservation: DataPreservation.OFF,
  algorithm: Algorithm.ANGEL,
  neighbour: 0, // stands for index in NEIGHBOUR_MARKS_ARR, not value
};
export const NEIGHBOUR_MARKS_ARR = ['10', '20', '30', '10%', '30%'];
const TEXT_TOOLTIP_ALGORITHM = 'Choose between different embedding algrotihms.';
const TEXT_TOOLTIP_NEIGHBOURS = 'The k-nearest neighborhood selection, used to construct an adjacency matrix.';
const TEXT_TOOLTIP_DATA_PRESERVATION = 'The red lines link the wrongly preserved local neighbourhood errors.';

export interface SettingsProps {
  settingsCommon: SettingsCommon;
  setSettingsCommon: React.Dispatch<React.SetStateAction<SettingsCommon>>;
  settingsCOVA: SettingsCOVA;
  setSettingsCOVA: React.Dispatch<React.SetStateAction<SettingsCOVA>>;
  settingsANGEL: SettingsANGEL;
  setSettingsANGEL: React.Dispatch<React.SetStateAction<SettingsANGEL>>;
  backLink: string;
  customDataPage?: CustomProps | null;
  reviewer: boolean;
  name: string;
  isLoading?: boolean;
}

const Settings = ({
  settingsCommon,
  setSettingsCommon,
  settingsCOVA,
  setSettingsCOVA,
  settingsANGEL,
  setSettingsANGEL,
  backLink,
  customDataPage,
  reviewer,
  name,
  isLoading,
}: SettingsProps) => {
  const onChangeAlgorithm = (event: React.ChangeEvent, newAlgorithm: Algorithm) => {
    event.preventDefault();
    setSettingsCommon((prev) => ({ ...prev, algorithm: newAlgorithm }));
  };
  const onChangeNeighbour = (value: number) => setSettingsCommon((prev) => ({ ...prev, neighbour: value }));
  const onChangeDataPreservation = (event: React.ChangeEvent, value: DataPreservation) => {
    event.preventDefault();
    setSettingsCommon((prev) => ({ ...prev, dataPreservation: value }));
  };

  const [height, setHeight] = useState(0);
  const refIndex = useRef() as React.MutableRefObject<HTMLDivElement>;
  const [margin, setMargin] = useState(0);
  const refNeighbours = useRef() as React.MutableRefObject<HTMLDivElement>;

  useEffect(() => {
    setHeight(refIndex.current.scrollHeight);
    setMargin(refNeighbours.current.offsetTop - 10);
  });

  const entriesAlgorithm = customDataPage
    ? [
        { value: Algorithm.COVA, text: TEXT_CHECKBOX_COVA },
        { value: Algorithm.ANGEL, text: TEXT_CHECKBOX_ANGEL },
      ]
    : [
        { value: Algorithm.COVA, text: TEXT_CHECKBOX_COVA },
        { value: Algorithm.ANGEL, text: TEXT_CHECKBOX_ANGEL },
        { value: Algorithm.ORIGINAL, text: TEXT_CHECKBOX_ORIGINAL },
      ];
  return (
    <div className={classes.index} ref={refIndex}>
      <LinkBack link={backLink} block />
      <div className={classes.Settings}>
        <h1>{name}</h1>
        {!reviewer && (
          <CheckBoxes
            labelText={TEXT_CHECKBOX_ALGORITHM}
            tooltipText={TEXT_TOOLTIP_ALGORITHM}
            currentValue={settingsCommon.algorithm}
            onChange={onChangeAlgorithm}
            entries={entriesAlgorithm}
          />
        )}
        <Slider
          min={0}
          max={NEIGHBOUR_MARKS_ARR.length - 1}
          step={1}
          marksArr={NEIGHBOUR_MARKS_ARR}
          onChange={onChangeNeighbour}
          labelText={TEXT_SLIDER_NEIGHBOUR}
          tooltipText={TEXT_TOOLTIP_NEIGHBOURS}
          value={settingsCommon.neighbour}
          refCustom={refNeighbours}
        />
        {settingsCommon.algorithm === Algorithm.COVA ? (
          <COVA {...{ settingsCOVA, setSettingsCOVA }} />
        ) : (
          <ANGEL {...{ settingsANGEL, setSettingsANGEL, isCustomDataPage: !!customDataPage }} />
        )}
        <CheckBoxes
          labelText={TEXT_CHECKBOX_PRESERVATION}
          tooltipText={TEXT_TOOLTIP_DATA_PRESERVATION}
          currentValue={settingsCommon.dataPreservation}
          onChange={onChangeDataPreservation}
          entries={[
            { value: DataPreservation.ON, text: 'Yes' },
            { value: DataPreservation.OFF, text: 'No' },
          ]}
        />
        {customDataPage && <Custom {...customDataPage} />}
        {isLoading && <Loader height={height} />}
        {settingsCommon.algorithm === Algorithm.ORIGINAL && <ModalWithFit height={height - margin} margin={margin} />}
      </div>
    </div>
  );
};

Settings.defaultProps = {
  settingsCustom: null,
  isLoading: false,
};

export default Settings;
