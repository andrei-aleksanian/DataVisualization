import { Canvas } from '@react-three/fiber';

import Controls from './Controls';
import Scene from './Scene';

import classes from './Visualization2D.module.scss';
import { Data2DColored } from '../types/Data';

const Visualization2D = ({ data }: { data: Data2DColored }) => {
  return (
    <Canvas camera={{ position: [0, 0, 100] }}>
      <Controls />
      <Scene data={data} dimension2D={data.dimension2D} />
    </Canvas>
  );
};

const Wrapper = ({ data }: { data: Data2DColored }) => (
  <div className={classes.Canvas}>
    <Visualization2D data={data} />
  </div>
);

export default Wrapper;
