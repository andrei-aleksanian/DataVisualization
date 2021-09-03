import { LinkHero } from 'Components/Link';
import classes from './Home.module.scss';

export const TEXT_LINK_EXAMPLES = 'See an Example';
export const TEXT_LINK_CUSTOM_DATA = 'Visualize Your Data';

export const TEXT_H1 = 'COVA/ANGEL Visualization';
export const TEXT_P =
  'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Delectus dolorum laudantium nisi cupiditate pariatur odio deserunt sunt beatae nostrum tempore cumque iusto, quas ducimus vitae voluptatem repudiandae animi, repellendus commodi! Lorem ipsum dolor sit, amet consectetur adipisicing elit. Delectus dolorum laudantium nisi cupiditate pariatur odio deserunt sunt beatae nostrum tempore cumque iusto, quas ducimus vitae voluptatem repudiandae animi, repellendus commodi!';

const Home = () => {
  return (
    <div className={classes.index}>
      <div className={classes.Container}>
        <h1>{TEXT_H1}</h1>
        <p>{TEXT_P}</p>
        <div className={classes.LinkWrapper}>
          <LinkHero text={TEXT_LINK_EXAMPLES} link="/examples" />
          <LinkHero text={TEXT_LINK_CUSTOM_DATA} link="/your-data" />
        </div>
      </div>
    </div>
  );
};

export default Home;
