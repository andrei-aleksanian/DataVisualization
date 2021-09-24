import { Line } from '@react-three/drei';
import { DataPerseveranceColored } from 'types/Data/DataPerseverance';
import getId from 'utils/getId';
import Point from './Point';
import { getRadius } from './utils';

export interface SceneProps {
  data: DataPerseveranceColored;
  showPreservation: boolean;
}

export default function Scene({
  data: { colors, points, prevPartsave, prevWrongInLow, dimension2D },
  showPreservation,
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
          key={getId('point')}
          radius={getRadius(prevPartsave.includes(i) && showPreservation)}
          isPreservation={showPreservation}
        />
      ))}
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
