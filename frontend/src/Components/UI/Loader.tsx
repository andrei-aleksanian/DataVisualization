import { ModalWithFit } from './Modal';

import classes from './UI.module.scss';

const Loader = ({ height }: { height: number }) => {
  return (
    <ModalWithFit height={height}>
      <div className={classes.loader}>Loading...</div>
    </ModalWithFit>
  );
};

export default Loader;
