import { useRef, useEffect, useState } from 'react';
import cx from 'classnames';

import info from 'Components/assets/info.svg';

import getId from 'utils/getId';
import classes from './Label.module.scss';

export interface LabelProps {
  text: string;
  tooltipText: string;
  customCalss?: string;
  link?: JSX.Element; // accepts an anchor tag, not sure how to type it
}

const Label = ({ text, customCalss, tooltipText, link }: LabelProps) => {
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
        <div style={{ top: top + 19, left: left - 115 }}>
          {tooltipText} {link}
        </div>
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
