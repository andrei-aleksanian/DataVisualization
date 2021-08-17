import { Line } from '@react-three/drei';
import { DataPerseveranceColored } from 'types/Data/DataPerseverance';
import Point from './Point';
import { getRadius, getId } from './utils';

export interface SceneProps {
  data: DataPerseveranceColored;
  dimension2D: boolean;
}

export default function Scene({
  data: { colors, points, prevPartsave, prevWrongInLow, prevWrongInHigh },
  dimension2D,
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
          // eslint-disable-next-line react/no-array-index-key
          key={getId()}
          radius={getRadius(prevPartsave.includes(i))}
        />
      ))}
      {prevPartsave.map((i) => {
        const pointFrom = points[i];
        return prevWrongInLow[i].map((p) => {
          const pointTo = points[p];
          return <Line points={[pointFrom, pointTo]} color="red" lineWidth={1} dashed={false} key={getId('line')} />;
        });
      })}
      {prevPartsave.map((i) => {
        const pointFrom = points[i];
        return prevWrongInHigh[i].map((p) => {
          const pointTo = points[p];
          return <Line points={[pointFrom, pointTo]} color="blue" lineWidth={1} dashed key={getId('line')} />;
        });
      })}
    </>
  );
}
