import Button from '../Components/Forms/Button';

import { Algorithm, SettingsInterface } from '../types/Settings';

import classes from './Settings.module.scss';

export const H1_TEXT = 'Demo Version';

export interface SettingsProps {
  setSettigns: React.Dispatch<React.SetStateAction<SettingsInterface>>;
  runAlgorithm: (e: React.MouseEvent) => Promise<void>;
  currentAlgorithm: Algorithm;
}

const Settings = ({ setSettigns, runAlgorithm, currentAlgorithm }: SettingsProps) => {
  const onClick = (event: React.MouseEvent, algorithm: Algorithm) => {
    event.preventDefault();
    setSettigns(() => ({
      algorithm,
    }));
  };

  return (
    <div className={classes.Settings}>
      <h1 className={classes.Heading}>{H1_TEXT}</h1>
      <div className={classes.ButtonsBox}>
        <Button
          text="COVA"
          onClick={(e) => {
            onClick(e, Algorithm.COVA);
          }}
          active={currentAlgorithm === Algorithm.COVA}
        />
        <Button
          text="ANGEL"
          onClick={(e) => {
            onClick(e, Algorithm.ANGEL);
          }}
          active={currentAlgorithm === Algorithm.ANGEL}
        />
      </div>
      <Button
        text="COVA3D"
        onClick={(e) => {
          onClick(e, Algorithm.COVA_PESEVERANCE);
        }}
        active={currentAlgorithm === Algorithm.COVA_PESEVERANCE}
        center
      />
      <Button
        text="Run the demo!"
        onClick={(e) => runAlgorithm(e)}
        customClass={classes.LongButton}
        long
        center
        active={false}
      />
    </div>
  );
};

export default Settings;
