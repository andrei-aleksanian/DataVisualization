import { useEffect, useState } from 'react';
import { LinkBack } from 'Components/Link';
import { ExampleProps } from 'types/Examples';

import { useHistory } from 'react-router-dom';
import getId from 'utils/getId';
import { Popup } from 'Components/UI';
import fetchExamples from './services';

import classes from './Library.module.scss';

export const TEXT_H1 = 'Examples Library';
export const TEXT_POPUP = "Couldn't load examples, please try again later";

const Library = () => {
  const [examples, setExamples] = useState([] as ExampleProps[]);
  const [error, setError] = useState(null as null | string);
  const history = useHistory();

  const Example = ({ name, description, id, imagePath }: ExampleProps) => (
    <div className={classes.Example}>
      <img
        src={`http://localhost:8080/images/${imagePath}`}
        alt={`example ${name} image`}
        onClick={() => history.push(`/examples/${id}`)}
      />
      <div className={classes.ExampleInfo}>
        <h3>{name}</h3>
        <p>{description}</p>
      </div>
    </div>
  );

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
      <LinkBack link="/" />
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
