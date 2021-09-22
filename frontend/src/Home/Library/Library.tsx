import { useEffect, useState } from 'react';
import { LinkBack } from 'Components/Link';
import { ExampleProps } from 'types/Examples';

import { useHistory, useLocation } from 'react-router-dom';
import getId from 'utils/getId';
import hostLink from 'utils/hostLink';
import { Popup } from 'Components/UI';
import Button from 'Components/Forms/Button';
import fetchExamples from './services';

import classes from './Library.module.scss';

export const TEXT_H1 = 'Examples Library';
export const TEXT_POPUP = "Couldn't load examples, please try again later";
export interface LibraryProps {
  reviewer: boolean;
}
const Library = ({ reviewer }: LibraryProps) => {
  const [examples, setExamples] = useState([] as ExampleProps[]);
  const [error, setError] = useState(null as null | string);
  const history = useHistory();
  const location = useLocation();

  const Example = ({ name, description, id, imagePath }: ExampleProps) => {
    const onClickExample = () => history.push(`${location.pathname}/${id}`);
    return (
      <div className={classes.Example}>
        <img src={`${hostLink}/api/images/${imagePath}`} alt={`example ${name} image`} onClick={onClickExample} />
        <div className={classes.ExampleInfo}>
          <h3>{name}</h3>
          <p>{description}</p>
          <Button text="See Example" onClick={onClickExample} active customClass={classes.Button} />
        </div>
      </div>
    );
  };

  useEffect(() => {
    let isActive = true;
    const getExamples = async () => {
      const [data, newError] = await fetchExamples();

      if (!isActive) return;
      if (data) setExamples(data);
      setError(newError);
    };
    getExamples();

    return () => {
      isActive = false;
    };
  }, []);

  return (
    <div className={classes.index}>
      {error && <Popup text={TEXT_POPUP} onClick={() => history.push('/')} />}
      {!reviewer && <LinkBack link="/" />}
      <h1>{TEXT_H1}</h1>
      <div className={classes.ExamplesContainer}>
        {examples.map((e) => (
          <Example {...e} key={getId('example')} />
        ))}
      </div>
    </div>
  );
};

export default Library;
