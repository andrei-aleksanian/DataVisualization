import Button from 'Components/Forms/Button';
import Modal from './Modal';
import classes from './UI.module.scss';

export interface PopupProps {
  text: string;
  onClick: Function;
}

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

export default Popup;
