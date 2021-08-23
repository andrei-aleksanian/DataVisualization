import { Canvas } from '@react-three/fiber';
import { TrackballControls } from '@react-three/drei';

import { DataPerseveranceColored } from 'types/Data/DataPerseverance';
import Scene from './Scene';

import classes from './Visualization2D.module.scss';

const Visualization2D = ({ data }: { data: DataPerseveranceColored }) => {
  return (
    <Canvas camera={{ position: [0, 0, 100] }}>
      <TrackballControls />
      <Scene data={data} dimension2D={data.dimension2D} />
    </Canvas>
  );
};

const Wrapper = ({ data }: { data: DataPerseveranceColored }) => (
  <div className={classes.Canvas}>
    <Visualization2D data={data} />
  </div>
);

export default Wrapper;
