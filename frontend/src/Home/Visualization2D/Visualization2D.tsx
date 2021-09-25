import { Canvas } from '@react-three/fiber';
import { OrbitControls, MapControls } from '@react-three/drei';
import { ResizeObserver } from '@juggle/resize-observer';

import { DataPerseveranceColored } from 'types/Data/DataPerseverance';
import Scene from './Scene';

import classes from './Visualization2D.module.scss';

export interface Visualization2DProps {
  data: DataPerseveranceColored;
  showPreservation: boolean;
}

const Visualization2D = ({ data, ...props }: Visualization2DProps) => {
  return (
    <Canvas camera={{ position: [0, 0, 100] }} resize={{ polyfill: ResizeObserver }}>
      {data.dimension2D ? <MapControls enableRotate={false} zoomSpeed={0.3} /> : <OrbitControls zoomSpeed={0.3} />}
      <Scene {...props} data={data} />
    </Canvas>
  );
};

const Wrapper = (props: Visualization2DProps) => (
  <div className={classes.Canvas} data-testid="canvas">
    <Visualization2D {...props} />
  </div>
);

export default Wrapper;
