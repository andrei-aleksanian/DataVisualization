import { useState } from 'react';

import Visualization2D from './Visualization2D';
import Settings from './Settings';

import { Algorithm, defaultSettings } from './types/Settings';
import { Point2D, Point3D } from './types/Data';
import { DataPerseveranceLabelled, DataPerseveranceColored } from './types/Data/DataPerseverance';
import { getCovaDemo2, getCovaDemo2Init } from './utils/services';
import getColors, { colorPartsave } from './utils/getColors';

import classes from './App.module.scss';

const App = () => {
  const [settings, setSettings] = useState(defaultSettings);
  const [data, setData] = useState<DataPerseveranceColored | null>(null);

  const runAlgorithm = async (event: React.MouseEvent) => {
    const updateData = (newData: DataPerseveranceLabelled) => {
      setData((prev) => {
        if (prev === null) console.log(newData);
        let colors = prev === null ? getColors(newData.labels) : prev.colors;
        colors = colorPartsave(newData.prevPartsave, colors);
        return {
          ...newData,
          points: newData.points.map((p) => p.map((p2) => p2 * 50) as Point2D | Point3D),
          colors,
        };
      });
    };

    event.preventDefault();

    let newData;
    if (settings.algorithm === Algorithm.COVA_PERSEVERANCE) {
      newData = await getCovaDemo2Init();
      updateData(newData);
      while (newData.iteration < newData.maxIteration) {
        /* eslint-disable no-await-in-loop */
        newData = await getCovaDemo2(newData.iteration, newData);
        await updateData(newData);
      }
    }
  };

  return (
    <div className={classes.App}>
      <Settings setSettigns={setSettings} runAlgorithm={runAlgorithm} currentAlgorithm={settings.algorithm} />
      {data && <Visualization2D data={data} />}
    </div>
  );
};

export default App;
