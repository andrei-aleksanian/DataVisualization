// import { useState } from 'react';
import { LinkBack } from 'Components/Link';
import classes from './Custom.module.scss';

const Custom = () => {
  // const [data, setData] = useState<DataPerseveranceColored | null>(null);

  // const runAlgorithm = async (event: React.MouseEvent, algorithm: Algorithm) => {
  //   const updateData = (newData: DataPerseveranceLabelled) => {
  //     setData((prev) => {
  //       let colors = prev === null ? getColors(newData.labels) : prev.colors;
  //       colors = colorPartsave(newData.prevPartsave, colors);
  //       return {
  //         ...newData,
  //         points: newData.points.map((p) => p.map((p2) => p2 * 100) as Point2D | Point3D),
  //         colors,
  //       };
  //     });
  //   };

  //   event.preventDefault();

  //   let newData;
  //   if (algorithm === Algorithm.COVA) {
  //     newData = await getCovaDemo2Init();
  //     updateData(newData);
  //     while (newData.iteration < newData.maxIteration) {
  //       /* eslint-disable no-await-in-loop */
  //       newData = await getCovaDemo2(newData.iteration, newData);
  //       await updateData(newData);
  //     }
  //   } else if (algorithm === Algorithm.ANGEL) {
  //     // call angel endpoint init
  //     // while loop call angel dynamic function
  //   }
  // };
  return (
    <div className={classes.index}>
      <div>
        <p>Sorry, this page is not implemented yet!</p>
        <LinkBack link="/" />
      </div>
    </div>
  );
};

export default Custom;
