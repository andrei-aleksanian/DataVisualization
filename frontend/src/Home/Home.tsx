import { LinkHero } from 'Components/Link';
import classes from './Home.module.scss';

const Home = () => {
  return (
    <div className={classes.index}>
      <div className={classes.Container}>
        <h1>COVA/ANGEL Visualization</h1>
        <p>
          Lorem ipsum dolor sit, amet consectetur adipisicing elit. Delectus dolorum laudantium nisi cupiditate pariatur
          odio deserunt sunt beatae nostrum tempore cumque iusto, quas ducimus vitae voluptatem repudiandae animi,
          repellendus commodi! Lorem ipsum dolor sit, amet consectetur adipisicing elit. Delectus dolorum laudantium
          nisi cupiditate pariatur odio deserunt sunt beatae nostrum tempore cumque iusto, quas ducimus vitae voluptatem
          repudiandae animi, repellendus commodi!
        </p>
        {/* Need bigger buttons here */}
        <LinkHero text="See an Example" link="/examples" />
        <LinkHero text="Visualize Your Data" link="/your-data" />
      </div>
    </div>
  );
};

export default Home;
