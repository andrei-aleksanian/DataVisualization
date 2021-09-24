/*
Slider Component.

All intended uses imply marks on the slider, but the slider is highly customizable.
See rc-slider https://www.npmjs.com/package/rc-slider for more details.

Unfortunately, this library doesn't support css modules very well,
so all css is hardcoded inside style elements.
*/
import { CSSProperties } from 'react';
import SliderRC from 'rc-slider';

import toMarks from './utils';
import Label from '../Label';
import classes from './Slider.module.scss';

export interface SliderProps {
  onChange: (value: number) => void;
  min: number;
  max: number;
  step: number | null;
  marksArr: (number | string)[];
  labelText: string;
  tooltipText: string;
  value: number;
  refCustom?: React.MutableRefObject<HTMLDivElement> | 0;
}

const Slider = ({ marksArr, labelText, tooltipText, refCustom, ...restProps }: SliderProps) => {
  const marksStyle = {
    fontSize: '0.85rem',
    color: '#ccc',
  } as CSSProperties;

  const handleStyle = {
    borderColor: 'var(--color-action)',
    height: 20,
    width: 20,
    marginTop: -9,
    backgroundColor: 'var(--color-action)',
    boxShadow: 'none',
  };
  const railStyle = { backgroundColor: 'var(--color-text)', height: 4 };
  const trackStyle = { backgroundColor: 'var(--color-action)', height: 4 };
  const dotStyle = { border: '2px solid #fff', height: 10, width: 10, bottom: -3 };
  const activeDotStyle = { border: '2px solid var(--color-action)', backgroundColor: 'var(--color-action)' };

  return (
    <div className={classes.index} ref={refCustom !== 0 ? refCustom : null}>
      <Label text={labelText} tooltipText={tooltipText} />
      <SliderRC
        {...restProps}
        marks={toMarks(marksArr, marksStyle)}
        handleStyle={handleStyle}
        railStyle={railStyle}
        trackStyle={trackStyle}
        dotStyle={dotStyle}
        activeDotStyle={activeDotStyle}
      />
    </div>
  );
};

Slider.defaultProps = {
  refCustom: 0,
};

export default Slider;
