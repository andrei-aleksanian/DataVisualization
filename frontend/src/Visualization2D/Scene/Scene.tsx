import { DataColored } from '../../types/Data/Data';
import { Point2D, Point3D } from './points';

export interface PointProps {
  x: number;
  y: number;
  z: number;
  color: string;
}

export interface SceneProps {
  data: DataColored;
  dimension2D: boolean;
}

export default function Scene({ data: { colors, points }, dimension2D }: SceneProps) {
  return (
    <>
      <ambientLight color="#fff" intensity={1.0} />
      {points.map((p, i) => (
        <>
          {dimension2D ? (
            <Point2D x={p[0]} y={p[1]} z={p[2]} color={`#${colors[i]}`} key={`${p[0]}${p[1]}${p[2]}`} />
          ) : (
            <Point3D x={p[0]} y={p[1]} z={p[2]} color={`#${colors[i]}`} key={`${p[0]}${p[1]}${p[2]}`} />
          )}
        </>
      ))}
    </>
  );
}
