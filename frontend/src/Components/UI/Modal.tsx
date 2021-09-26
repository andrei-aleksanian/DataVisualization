import cx from 'classnames';

import classes from './UI.module.scss';

export const ModalWithFit = ({
  children,
  height,
  customClass,
  margin,
}: {
  children?: JSX.Element;
  height: number;
  customClass?: string;
  margin?: number;
}) => {
  return (
    <>
      <div
        className={cx(classes.Modal, classes.ModalFill, classes.ModalWithFit, customClass)}
        style={{ height, marginTop: margin }}
      />
      <div className={classes.ModalWithFit} style={{ height, marginTop: margin }}>
        {children}
      </div>
    </>
  );
};
ModalWithFit.defaultProps = {
  children: <div />,
  customClass: '',
  margin: 0,
};

const Modal = ({ hide }: { hide: Function }) => {
  return <div className={classes.Modal} onClick={() => hide()} />;
};

export default Modal;
