/**
 * Checkboxes - radio buttons.
 *
 * Used for displaying an array of checkboxes
 * that bind to state of the parent component.
 *
 * @param entries - array of checkboxes to be generated
 * @param currentValue - current value of the state from parent component
 * @param onChange - function that handles a ckick on any checkbox
 * @param labelText - text to describe the group of checkboxes. e.g. 'Checkboxes:'
 */

import getId from 'utils/getId';
import Label from '../Label';
import classes from './CheckBoxes.module.scss';

export interface CheckBoxesProps {
  entries: { value: number; text: string }[];
  currentValue: number;
  onChange: (event: React.ChangeEvent, currentValue: number) => void;
  labelText: string;
  tooltipText: string;
}

const CheckBoxes = ({ currentValue, onChange, entries, labelText, tooltipText }: CheckBoxesProps) => (
  <div className={classes.index}>
    <Label text={labelText} tooltipText={tooltipText} />
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
