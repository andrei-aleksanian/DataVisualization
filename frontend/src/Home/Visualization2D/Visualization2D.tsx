import { Canvas } from '@react-three/fiber';
import { TrackballControls } from '@react-three/drei';

import { DataPerseveranceColored } from 'types/Data/DataPerseverance';
import Scene from './Scene';

import classes from './Visualization2D.module.scss';

export interface Visualization2DProps {
  data: DataPerseveranceColored;
  showPreservation: boolean;
  colorPreservation: () => void;
}

const Visualization2D = ({ data, ...props }: Visualization2DProps) => {
  return (
    <Canvas camera={{ position: [0, 0, 100] }}>
      <TrackballControls />
      <Scene {...props} dimension2D={data.dimension2D} data={data} />
    </Canvas>
  );
};

const Wrapper = (props: Visualization2DProps) => (
  <div className={classes.Canvas}>
    <Visualization2D {...props} />
  </div>
);

export default Wrapper;
