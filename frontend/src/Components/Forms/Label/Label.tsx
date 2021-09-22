import { useRef, useEffect, useState } from 'react';
import cx from 'classnames';

import info from 'Components/assets/info.svg';

import getId from 'utils/getId';
import classes from './Label.module.scss';

export interface LabelProps {
  text: string;
  tooltipText: string;
  customCalss?: string;
}

const Label = ({ text, customCalss, tooltipText }: LabelProps) => {
  const Tooltip = () => {
    const [top, setTop] = useState(0);
    const [left, setLeft] = useState(0);
    const ref = useRef() as React.MutableRefObject<HTMLImageElement>;

    useEffect(() => {
      setTop(ref.current.offsetTop);
      setLeft(ref.current.offsetLeft);
    }, []);

    return (
      <div className={classes.Tooltip}>
        <img src={info} alt={getId('info')} ref={ref} />
        <div style={{ top: top + 20, left: left - 120 }}>{tooltipText}</div>
      </div>
    );
  };

  return (
    <div className={cx(classes.index, customCalss)}>
      <p>{text}</p>
      <Tooltip />
    </div>
  );
};

Label.defaultProps = {
  customClass: '',
};

export default Label;
