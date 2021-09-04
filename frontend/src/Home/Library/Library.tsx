import { useEffect, useState } from 'react';
import { LinkBack } from 'Components/Link';
import { ExampleProps } from 'types/Examples';

import { useHistory } from 'react-router-dom';
import fetchExamples from './services';

import classes from './Library.module.scss';

const Library = () => {
  const [examples, setExamples] = useState([] as ExampleProps[]);
  const history = useHistory();

  const Example = ({ name, description, id }: ExampleProps) => (
    <div className={classes.Example}>
      <img
        src="https://picsum.photos/350/200"
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
    const getExamples = async () => {
      const data = await fetchExamples();
      setExamples(data);
    };
    getExamples();
  }, []);

  return (
    <div className={classes.index}>
      <LinkBack link="/" />
      {examples.map((e) => (
        <Example {...e} />
      ))}
    </div>
  );
};

export default Library;
