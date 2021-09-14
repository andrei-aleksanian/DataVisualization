import { Switch, Route } from 'react-router-dom';
import Library from 'Home/Library';
import Home from './Home';
import Examples from './Home/Examples';
import Custom from './Home/Custom';

export default function App() {
  return (
    <Switch>
      <Route path="/demo-review/:id">
        <Examples reviewer backLink="/demo-review" />
      </Route>
      <Route path="/demo-review">
        <Library reviewer />
      </Route>
      <Route path="/examples/:id">
        <Examples reviewer={false} backLink="/examples" />
      </Route>
      <Route path="/examples">
        <Library reviewer={false} />
      </Route>
      <Route path="/your-data">
        <Custom />
      </Route>
      <Route path="/">
        <Home />
      </Route>
    </Switch>
  );
}
