// import { Formik, Form, useField } from 'formik';
import { useState } from 'react';
import { LinkBack } from 'Components/Link';
import Slider from 'Components/Forms/Slider';

import { Algorithm } from 'types/Settings';
import CheckBoxes from './components/CheckBoxes';

import classes from './Settings.module.scss';

export const H1_TEXT = 'Example: Cylinder';

export enum C {
  ORIGINAL,
  PERCENTAGE,
}

interface SettingsCOVA {
  neighbour: number;
  lambda: number;
  alpha: number;
  c: C;
}

export const defaultSettingsCOVA: SettingsCOVA = {
  neighbour: 10,
  lambda: 0,
  alpha: 0,
  c: C.ORIGINAL,
};

const Settings = () => {
  const [algorithm, setAlgorithm] = useState(Algorithm.COVA);
  // const [dataPreservation, setDataPreservation] = useState(false);
  const [settingsCOVA, setSettingsCOVA] = useState(defaultSettingsCOVA);
  const onClickAlgorithm = (event: React.ChangeEvent, newAlgorithm: Algorithm) => {
    event.preventDefault();
    setAlgorithm(() => newAlgorithm);
  };

  const onChangeNeighbour = (value: number) => setSettingsCOVA((prev) => ({ ...prev, neighbour: value }));
  const onChangeLambda = (value: number) => setSettingsCOVA((prev) => ({ ...prev, lambda: value }));
  const onChangeAlpha = (value: number) => setSettingsCOVA((prev) => ({ ...prev, alpha: value }));

  return (
    <div className={classes.Settings}>
      <LinkBack link="/" />
      <h1>{H1_TEXT}</h1>
      <CheckBoxes key={algorithm} currentAlgorithm={algorithm} onClickAlgorithm={onClickAlgorithm} />
      <Slider
        min={10}
        max={100}
        step={10}
        marksArr={[10, 20, 30, 40, 50, 60, 70, 80, 90, 100]}
        onChange={onChangeNeighbour}
        text="Neighbour"
        value={settingsCOVA.neighbour}
      />
      <Slider
        min={0}
        max={1}
        step={0.2}
        marksArr={[0, 0.2, 0.4, 0.6, 0.8, 1]}
        onChange={onChangeLambda}
        text="Lambda"
        value={settingsCOVA.lambda}
      />
      <Slider
        min={0}
        max={1}
        step={0.2}
        marksArr={[0, 0.2, 0.4, 0.6, 0.8, 1]}
        onChange={onChangeAlpha}
        text="Alpha"
        value={settingsCOVA.alpha}
      />
    </div>
  );
};

export default Settings;
