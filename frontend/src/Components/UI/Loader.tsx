import { ModalWithFit } from './Modal';

import classes from './UI.module.scss';

const Loader = ({ height }: { height: number }) => {
  return (
    <ModalWithFit height={height}>
      <div className={classes.LoaderWrapper}>
        <div className={classes.loader}>Loading...</div>
        <p>We are processing your data...</p>
      </div>
    </ModalWithFit>
  );
};

export default Loader;
