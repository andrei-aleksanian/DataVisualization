/*
Slider Component.

All intended uses imply marks on the slider, but the slider is highly customizable.
See rc-slider https://www.npmjs.com/package/rc-slider for more details.
*/

import SliderRC from 'rc-slider';
import classes from './Slider.module.scss';
import 'rc-slider/assets/index.css';
import toMarks from './utils';

export interface SliderProps {
  onChange: (value: number) => void;
  min: number;
  max: number;
  step: number | null;
  marksArr: number[];
  text: string;
  value: number;
}

const Slider = ({ marksArr, text, ...restProps }: SliderProps) => (
  <div className={classes.index}>
    <p>{text}</p>
    <SliderRC {...restProps} marks={toMarks(marksArr)} />
  </div>
);

export default Slider;
