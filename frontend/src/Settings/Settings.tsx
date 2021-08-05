import Button from '../Components/Forms/Button';

import classes from './Settings.module.scss';

export const H1_TEXT = 'Demo Version';

export default function Settings() {
  return (
    <div className={classes.Settings}>
      <h1 className={classes.Heading}>{H1_TEXT}</h1>
      <div className={classes.ButtonsBox}>
        <Button text="COVA" onClick={() => {}} />
        <Button text="ANGEL" onClick={() => {}} />
      </div>
      <Button text="Run the demo!" onClick={() => {}} customClass={classes.LongButton} long center />
    </div>
  );
}
