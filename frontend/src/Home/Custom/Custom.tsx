import { LinkBack } from 'Components/Link';
import classes from './Custom.module.scss';

const Custom = () => {
  return (
    <div className={classes.index}>
      <div>
        <p>Sorry, this page is not implemented yet!</p>
        <LinkBack link="/" />
      </div>
    </div>
  );
};

export default Custom;
