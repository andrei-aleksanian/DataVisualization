import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Home from './Home';
import Examples from './Home/Examples';
import Custom from './Home/Custom';

export default function App() {
  return (
    <Router>
      <Switch>
        <Route path="/examples">
          <Examples />
        </Route>
        <Route path="/your-data">
          <Custom />
        </Route>
        <Route path="/">
          <Home />
        </Route>
      </Switch>
    </Router>
  );
}
