/**
 * Button - highly customizable button.
 * Automatically centres or stretches to 100% width of the parent container.
 */

import cx from 'classnames';

import classes from './Button.module.scss';

interface ButtonProps {
  onClick: (event: React.MouseEvent) => void;
  text: string;
  customClass?: string;
  long?: boolean;
  active: boolean;
}

interface ButtonEnhancedProps extends ButtonProps {
  center?: boolean;
}
/**
 * Action Button. Bright red with white text.
 *
 * Button - the actual button component that always renders.
 *
 * WrapperCenter - wrapper that wraps the button and centers it in any div.
 * Only rendered if center prop is true. (Future reference - might move somewhere else)
 */
const ButtonEnhanced = (props: ButtonEnhancedProps) => {
  const WrapperCenter = ({ children }: { children: JSX.Element }) => (
    <div className={classes.WrapperCenter}>{children}</div>
  );

  const Button = ({ onClick, text, customClass, long, active }: ButtonProps) => {
    return (
      <button
        type="button"
        onClick={(e) => onClick(e)}
        className={cx(classes.Button, customClass, { [classes.Long]: long }, { [classes.active]: active })}
      >
        {text}
      </button>
    );
  };

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

export const defaultProps = {
  customClass: '',
  long: false,
  center: false,
};

ButtonEnhanced.defaultProps = defaultProps;

export default ButtonEnhanced;
