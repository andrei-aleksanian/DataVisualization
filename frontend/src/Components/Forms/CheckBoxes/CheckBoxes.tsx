/**
 * Checkboxes - radio buttons.
 *
 * Used for displaying an array of checkboxes
 * that bind to state of the parent component.
 *
 * @param entries - array of checkboxes to be generated
 * @param currentValue - current value of the state from parent component
 * @param onChange - function that handles a ckick on any checkbox
 * @param heading - text to describe the group of checkboxes. e.g. 'Checkboxes:'
 */

import getId from 'utils/getId';
import classes from './CheckBoxes.module.scss';

export interface CheckBoxesProps {
  entries: { value: number; text: string }[];
  currentValue: number;
  onChange: (event: React.ChangeEvent, currentValue: number) => void;
  heading: string;
}

const CheckBoxes = ({ currentValue, onChange, entries, heading }: CheckBoxesProps) => (
  <div className={classes.index}>
    <p>{heading}</p>
    <div className={classes.CheckBoxes}>
      {entries.map((e) => (
        <label key={getId('checkbox')}>
          <input type="radio" checked={currentValue === e.value} onChange={(event) => onChange(event, e.value)} />
          <span className={classes.text}>{e.text}</span>
          <span className={classes.checkmark} />
        </label>
      ))}
    </div>
  </div>
);

export default CheckBoxes;
