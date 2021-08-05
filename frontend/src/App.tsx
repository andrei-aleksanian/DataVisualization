import { useState } from 'react';
import Visualization2D from './Visualization2D';
import Settings from './Settings';

import { defaultSettings } from './types/Settings';
import { Data2DColored, Points2D } from './types/Data';
import { getAngelDemo } from './services';
import getColors from './utils/getColors';

import classes from './App.module.scss';

const App = () => {
  const [settings, setSettings] = useState(defaultSettings);
  const [data, setData] = useState<Data2DColored | null>(null);

  const runAlgorithm = async (event: React.MouseEvent) => {
    event.preventDefault();
    let newData = await getAngelDemo();

    newData = {
      labels: newData.labels,
      points: newData.points.map((p) => p.map((p2) => p2 * 50) as Points2D),
    };

    const dataColored: Data2DColored = {
      colors: getColors(newData.labels),
      points: newData.points,
    };
    setData(dataColored);
  };

  return (
    <div className={classes.App}>
      <Settings setSettigns={setSettings} runAlgorithm={runAlgorithm} currentAlgorithm={settings.algorithm} />
      {data && <Visualization2D data={data} />}
    </div>
  );
};

export default App;
