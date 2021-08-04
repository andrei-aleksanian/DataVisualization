import { useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';

import { Data2D, Data2DColored, Points2D } from '../types/Data';
import Controls from './Controls';
import Scene from './Scene';
import axios from '../utils/axios';

import classes from './Visualization2D.module.css';
import getColors from '../utils/getColors';

const Visualization2D: React.FC = () => {
  const [data, setData] = useState<Data2DColored | null>(null);

  useEffect(() => {
    const getData = async () => {
      let { data: newData }: { data: Data2D } = await axios.get('/angel-demo');

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
    getData();
  }, []);

  return (
    <Canvas camera={{ position: [0, 0, 100] }}>
      <Controls />
      {data && <Scene data={data} />}
    </Canvas>
  );
};

const Wrapper = () => (
  <div className={classes.Canvas}>
    <Visualization2D />
  </div>
);

export default Wrapper;
