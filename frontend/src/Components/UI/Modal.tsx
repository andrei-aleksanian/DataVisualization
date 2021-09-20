import cx from 'classnames';

import classes from './UI.module.scss';

export const ModalWithFit = ({ children, height }: { children: JSX.Element; height: number }) => {
  return (
    <>
      <div className={cx(classes.Modal, classes.ModalWithFit)} style={{ height }} />
      <div className={classes.ModalWithFit} style={{ height }}>
        {children}
      </div>
    </>
  );
};

const Modal = ({ hide }: { hide: Function }) => {
  return <div className={classes.Modal} onClick={() => hide()} />;
};

export default Modal;
