import { Canvas } from '@react-three/fiber';

import classes from './Visualization2D.module.css';
import { DATA } from '../types/Data';
import Controls from './Controls';
import Scene from './Scene';

const Visualization2D: React.FC = () => {
  return (
    <Canvas camera={{ position: [0, 0, 10] }}>
      <Controls />
      <Scene data={DATA} />
    </Canvas>
  );
};

const Wrapper = () => (
  <div className={classes.Canvas}>
    <Visualization2D />
  </div>
);

export default Wrapper;
