import { LinkHero } from 'Components/Link';
import classes from './Home.module.scss';

export const TEXT_LINK_LIBRARY = 'See an Example';
export const TEXT_LINK_CUSTOM_DATA = 'Visualize Your Data';

export const TEXT_H1 = 'COVA/ANGEL Visualization';
export const TEXT_P =
  "Dimensionality reduction for cohort data visualization is to plot a high-dimensional dataset in 2D,3D spaces to help analysts identify data properties and gain insights visually. COVA and ANGEL are two novel data visualization algorithms that provide a simple but effective way to improve cohort data visualization performance comprehensively. This demo website illustrates examples embedded by these two algorithms under different hyper-parameter settings and supports users in visualizing their datasets. In addition, the fast-ANGEL version is applied to the users' custom datasets. The current restriction of input data format is '.mat'.";
const Home = () => {
  return (
    <div className={classes.index}>
      <div className={classes.Container}>
        <h1>{TEXT_H1}</h1>
        <p>{TEXT_P}</p>
        <div className={classes.LinkWrapper}>
          <LinkHero text={TEXT_LINK_LIBRARY} link="/examples" />
          <LinkHero text={TEXT_LINK_CUSTOM_DATA} link="/your-data" />
        </div>
      </div>
    </div>
  );
};

export default Home;
