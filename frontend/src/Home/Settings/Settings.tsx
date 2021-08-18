// import { Formik, Form, useField } from 'formik';
import { useState } from 'react';
import { LinkBack } from 'Components/Link';

import { Algorithm, defaultSettings } from 'types/Settings';
import CheckBoxes from './components/CheckBoxes';

import classes from './Settings.module.scss';

export const H1_TEXT = 'Example: Cylinder';

const Settings = () => {
  const [settings, setSettings] = useState(defaultSettings);
  const onClickAlgorithm = (event: React.ChangeEvent, algorithm: Algorithm) => {
    event.preventDefault();
    setSettings(() => ({ algorithm }));
  };

  return (
    <div className={classes.Settings}>
      <LinkBack link="/" />
      <h1>{H1_TEXT}</h1>
      <CheckBoxes key={settings.algorithm} currentAlgorithm={settings.algorithm} onClickAlgorithm={onClickAlgorithm} />
    </div>
  );
};

export default Settings;
