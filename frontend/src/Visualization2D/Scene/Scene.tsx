import { DataPerseveranceColored } from '../../types/Data/DataPerseverance';
import { Point2D, Point3D } from './points';
import { getRadius } from './utils';

export interface SceneProps {
  data: DataPerseveranceColored;
  dimension2D: boolean;
}

export default function Scene({ data: { colors, points, prevPartsave }, dimension2D }: SceneProps) {
  return (
    <>
      <ambientLight color="#fff" intensity={1.0} />
      {points.map((p, i) => (
        <>
          {dimension2D ? (
            <Point2D
              x={p[0]}
              y={p[1]}
              z={p[2]}
              color={`#${colors[i]}`}
              // eslint-disable-next-line react/no-array-index-key
              key={`${p[0]}${p[1]}${p[2]}${i}`}
              radius={getRadius(i in prevPartsave)}
            />
          ) : (
            <Point3D
              x={p[0]}
              y={p[1]}
              z={p[2]}
              color={`#${colors[i]}`}
              // eslint-disable-next-line react/no-array-index-key
              key={`${p[0]}${p[1]}${p[2]}${i}`}
              radius={getRadius(i in prevPartsave)}
            />
          )}
        </>
      ))}
    </>
  );
}
