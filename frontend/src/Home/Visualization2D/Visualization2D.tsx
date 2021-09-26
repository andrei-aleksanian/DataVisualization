import { Canvas } from '@react-three/fiber';
import { OrbitControls, MapControls } from '@react-three/drei';
import { ResizeObserver } from '@juggle/resize-observer';

import { DataPerseveranceColored } from 'types/Data/DataPerseverance';
import { useRef } from 'react';
import Scene, { DEFAULT_CAM_POSITION } from './Scene';

import classes from './Visualization2D.module.scss';

export interface Visualization2DProps {
  data: DataPerseveranceColored;
  showPreservation: boolean;
  isViewReset: boolean;
}

const Visualization2D = ({ data, ...props }: Visualization2DProps) => {
  const controlsRef = useRef() as React.MutableRefObject<any>; // controls ref. Undocumented typing in r3f.
  return (
    <Canvas camera={{ position: DEFAULT_CAM_POSITION }} resize={{ polyfill: ResizeObserver }}>
      {data.dimension2D ? (
        <MapControls enableRotate={false} zoomSpeed={0.3} ref={controlsRef} />
      ) : (
        <OrbitControls zoomSpeed={0.3} ref={controlsRef} />
      )}
      <Scene {...props} data={data} controlsRef={controlsRef} />
    </Canvas>
  );
};

const Wrapper = (props: Visualization2DProps) => (
  <div className={classes.Canvas} data-testid="canvas">
    <Visualization2D {...props} />
  </div>
);

export default Wrapper;
