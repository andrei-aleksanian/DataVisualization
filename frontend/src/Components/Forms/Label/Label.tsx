import { useRef, useEffect, useState } from 'react';

import info from 'Components/assets/info.svg';

import classes from './Label.module.scss';

export interface LabelProps {
  text: string;
}

const Label = ({ text }: LabelProps) => {
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
        <img src={info} alt="back" ref={ref} />
        <div style={{ top, left: left + 30 }}>
          Choose how many points should the algorithm assume to have for neighbour separation
        </div>
      </div>
    );
  };
  return (
    <div className={classes.index}>
      <p>{text}</p>
      <Tooltip />
    </div>
  );
};

export default Label;
