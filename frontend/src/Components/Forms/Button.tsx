import cx from 'classnames';

import classes from './Button.module.scss';

interface ButtonProps {
  onClick: (event: React.MouseEvent) => void;
  text: string;
  customClass?: string;
  long?: boolean;
}

interface ButtonEnhancedProps extends ButtonProps {
  center?: boolean;
}

export const defaultProps = {
  customClass: '',
  long: false,
  center: false,
};

const ButtonEnhanced = (props: ButtonEnhancedProps) => {
  const WrapperCenter = ({ children }: { children: JSX.Element }) => {
    return <div className={classes.WrapperCenter}>{children}</div>;
  };

  const Button = ({ onClick, text, customClass, long }: ButtonProps) => (
    <button type="button" onClick={onClick} className={cx(classes.Button, customClass, { [classes.Long]: long })}>
      {text}
    </button>
  );

  Button.defaultProps = {
    customClass: '',
    long: false,
  };

  let output;

  if (props.center) {
    output = (
      <WrapperCenter>
        <Button {...props} />
      </WrapperCenter>
    );
  } else {
    output = <Button {...props} />;
  }

  return output;
};

ButtonEnhanced.defaultProps = defaultProps;

export default ButtonEnhanced;
