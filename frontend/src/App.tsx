import { Switch, Route } from 'react-router-dom';
import Library from 'Home/Library';
import Home from './Home';
import Examples from './Home/Examples';
import Custom from './Home/Custom';

export default function App() {
  return (
    <Switch>
      <Route path="/examples-for-review/:id">
        <Examples reviewer />
      </Route>
      <Route path="/examples/:id">
        <Examples reviewer={false} />
      </Route>
      <Route path="/examples">
        <Library />
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
