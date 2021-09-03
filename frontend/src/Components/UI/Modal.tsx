import classes from './UI.module.scss';

const Modal = ({ hide }: { hide: Function }) => {
  return <div className={classes.Modal} onClick={() => hide()} />;
};

export default Modal;
