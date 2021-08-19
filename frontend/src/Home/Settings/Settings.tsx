// import { Formik, Form, useField } from 'formik';
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

const Settings = () => {
  const [algorithm, setAlgorithm] = useState(Algorithm.COVA);
  const [dataPreservation, setDataPreservation] = useState(DataPreservation.OFF);
  const [settingsCOVA, setSettingsCOVA] = useState(defaultSettingsCOVA);
  const [settingsANGEL, setSettingsANGEL] = useState(defaultSettingsANGEL);

  const onChangeAlgorithm = (event: React.ChangeEvent, newAlgorithm: Algorithm) => {
    event.preventDefault();
    setAlgorithm(() => newAlgorithm);
  };
  const onChangeDataPreservation = (event: React.ChangeEvent, value: DataPreservation) => {
    event.preventDefault();
    setDataPreservation(() => value);
  };

  return (
    <div className={classes.index}>
      <LinkBack link="/" />
      <h1>{H1_TEXT}</h1>
      <CheckBoxes
        heading="Algorithm:"
        currentValue={algorithm}
        onChange={onChangeAlgorithm}
        entries={[
          { value: Algorithm.COVA, text: 'COVA' },
          { value: Algorithm.ANGEL, text: 'ANGEL' },
        ]}
      />
      {algorithm === Algorithm.COVA ? (
        <COVA {...{ settingsCOVA, setSettingsCOVA }} />
      ) : (
        <ANGEL {...{ settingsANGEL, setSettingsANGEL }} />
      )}
      <CheckBoxes
        heading="Show Data Preservation"
        currentValue={dataPreservation}
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
