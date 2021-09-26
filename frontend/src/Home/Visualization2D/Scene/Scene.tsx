import { useEffect } from 'react';
import { useThree } from '@react-three/fiber';
import { Line } from '@react-three/drei';
import { DataPerseveranceColored } from 'types/Data/DataPerseverance';
import getId from 'utils/getId';
import Point from './Point';
import { getRadius } from './utils';

export const DEFAULT_CAM_POSITION = [0, 0, 100] as [x: number, y: number, z: number];

const Reset = ({ reset, controlsRef }: { reset: boolean; controlsRef: React.MutableRefObject<any> }) => {
  const { camera } = useThree();
  useEffect(() => {
    if (reset) {
      controlsRef.current.reset();
      camera.position.set(DEFAULT_CAM_POSITION[0], DEFAULT_CAM_POSITION[1], DEFAULT_CAM_POSITION[2]);
    }
  }, []);

  return null;
};
export interface SceneProps {
  data: DataPerseveranceColored;
  showPreservation: boolean;
  controlsRef: React.MutableRefObject<any>;
  isViewReset: boolean;
}

export default function Scene({
  data: { colors, points, prevPartsave, prevWrongInLow, dimension2D },
  showPreservation,
  controlsRef,
  isViewReset,
}: SceneProps) {
  return (
    <>
      <ambientLight color="#fff" intensity={1.0} />
      {points.map((p, i) => (
        <Point
          dimension2D={dimension2D}
          x={p[0]}
          y={p[1]}
          z={p[2]}
          color={colors[i]}
          key={getId('point') + p[0]}
          radius={getRadius(prevPartsave.includes(i) && showPreservation)}
          isPreservation={showPreservation}
        />
      ))}
      <Reset key={getId(`reset-${points[0][0]}`)} reset={dimension2D && isViewReset} controlsRef={controlsRef} />
      {showPreservation &&
        prevPartsave.map((i) => {
          const pointFrom = points[i];
          return prevWrongInLow[i].map((p) => {
            const pointTo = points[p];
            return <Line points={[pointFrom, pointTo]} color="red" lineWidth={1} dashed={false} key={getId('line')} />;
          });
        })}
    </>
  );
}
