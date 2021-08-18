import { Algorithm } from 'types/Settings';
import classes from './CheckBoxes.module.scss';

export interface CheckBoxesProps {
  currentAlgorithm: Algorithm;
  onClickAlgorithm: (event: React.ChangeEvent, algorithm: Algorithm) => void;
}

const CheckBoxes = ({ currentAlgorithm, onClickAlgorithm }: CheckBoxesProps) => (
  <div className={classes.index}>
    <p>Algorithm:</p>
    <div className={classes.CheckBoxes}>
      <label>
        <input
          type="radio"
          checked={currentAlgorithm === Algorithm.COVA}
          onChange={(e) => onClickAlgorithm(e, Algorithm.COVA)}
        />
        <span className={classes.text}>COVA</span>
        <span className={classes.checkmark} />
      </label>
      <label>
        <input
          type="radio"
          checked={currentAlgorithm === Algorithm.ANGEL}
          onChange={(e) => onClickAlgorithm(e, Algorithm.ANGEL)}
        />
        <span className={classes.text}>ANGEL</span>
        <span className={classes.checkmark} />
      </label>
    </div>
  </div>
);

export default CheckBoxes;
