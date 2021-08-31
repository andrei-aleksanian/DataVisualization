import { Line } from '@react-three/drei';
import { DataPerseveranceColored } from 'types/Data/DataPerseverance';
import getId from 'utils/getId';
import Point from './Point';
import { getRadius } from './utils';

export interface SceneProps {
  data: DataPerseveranceColored;
  dimension2D: boolean;
  showPreservation: boolean;
  colorPreservation: () => void;
}

export default function Scene({
  data: { colors, points, prevPartsave, prevWrongInLow, prevWrongInHigh },
  dimension2D,
  showPreservation,
  colorPreservation,
}: SceneProps) {
  if (showPreservation) colorPreservation();
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
      {showPreservation &&
        prevPartsave.map((i) => {
          const pointFrom = points[i];
          return prevWrongInHigh[i].map((p) => {
            const pointTo = points[p];
            return <Line points={[pointFrom, pointTo]} color="blue" lineWidth={1} dashed key={getId('line')} />;
          });
        })}
    </>
  );
}
