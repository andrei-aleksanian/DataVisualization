import Visualization2D from './Visualization2D';
import Settings from './Settings';

import classes from './App.module.scss';

const App = () => (
  <div className={classes.App}>
    <Settings />
    <Visualization2D />
  </div>
);

export default App;
