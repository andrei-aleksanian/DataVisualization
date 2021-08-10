import { Canvas } from '@react-three/fiber';

import Controls from './Controls';
import Scene from './Scene';

import classes from './Visualization2D.module.scss';
import { DataColored } from '../types/Data/Data';

const Visualization2D = ({ data }: { data: DataColored }) => {
  return (
    <Canvas camera={{ position: [0, 0, 100] }}>
      <Controls />
      <Scene data={data} dimension2D={data.dimension2D} />
    </Canvas>
  );
};

const Wrapper = ({ data }: { data: DataColored }) => (
  <div className={classes.Canvas}>
    <Visualization2D data={data} />
  </div>
);

export default Wrapper;
