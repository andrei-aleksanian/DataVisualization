import cx from 'classnames';
import classes from './Error.module.scss';

export interface ErrorProps {
  text: string;
  customClass?: string;
}

const Error = ({ text, customClass }: ErrorProps) => (
  <p className={cx(classes.index, customClass)} data-testid="custom-error">
    {text}
  </p>
);

Error.defaultProps = {
  customClass: '',
};

export default Error;
