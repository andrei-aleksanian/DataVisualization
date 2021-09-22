import { Link } from 'react-router-dom';
import cx from 'classnames';
import arrow from '../assets/arrow.svg';
import classes from './Link.module.scss';

interface LinkProps {
  link: string;
  customClass?: string;
}

interface LinkBackProps extends LinkProps {
  block?: boolean;
}

interface LinkHeroProps extends LinkProps {
  text: string;
}

export const defaultPropsLink = {
  customClass: '',
};

export const defaultPropsLinkBack = {
  ...defaultPropsLink,
  block: false,
};

/*
Big Hero Link. Used for call to Action. Rediercts the user to a page of your choice.
*/
export const LinkHero = ({ text, link, customClass }: LinkHeroProps) => {
  return (
    <Link to={link} className={cx(classes.index, classes.Action, customClass)}>
      {text}
    </Link>
  );
};
LinkHero.defaultProps = defaultPropsLink;

/*
Small link back with an arrow. Used to come back to a page of your choice.
Intended use is to go back but can accept any link.
*/
export const LinkBack = ({ link, customClass, block }: LinkBackProps) => (
  <Link to={link} className={cx(classes.index, classes.Back, { [classes.Block]: block }, customClass)}>
    <img src={arrow} alt="back" />
  </Link>
);
LinkBack.defaultProps = defaultPropsLinkBack;
