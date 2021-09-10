import Button from 'Components/Forms/Button';
import Modal from './Modal';
import classes from './UI.module.scss';

export interface PopupProps {
  text?: string;
  onClick: Function;
}

export const POPUP_TEXT = 'Oops, something went wrong. Please try again later.';

const Popup = ({ text, onClick }: PopupProps) => {
  return (
    <>
      <Modal hide={onClick} />
      <div className={classes.Popup}>
        <p>{text}</p>
        <Button onClick={() => onClick()} text="OK" active={false} customClass={classes.CustomButton} center />
      </div>
    </>
  );
};

Popup.defaultProps = {
  text: POPUP_TEXT,
};

export default Popup;
