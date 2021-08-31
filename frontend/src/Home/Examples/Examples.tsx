import { useState, useEffect } from 'react';

import { Algorithm } from 'types/Settings';
import { Point2D, Point3D } from 'types/Data';
import { DataPerseveranceLabelled, DataPerseveranceColored } from 'types/Data/DataPerseverance';
import getColors from 'utils/getColors';

import { ParamsCOVA } from 'types/Data/Params';
import { getDataCOVA } from './services';

import Settings, {
  defaultSettingsCOVA,
  defaultSettingsANGEL,
  defaultSettingsCommon,
  NEIGHBOUR_MARKS_ARR,
  C,
  DataPreservation,
} from '../Settings';
import Visualization2D from '../Visualization2D';

import classes from './Examples.module.scss';

const Examples = () => {
  const [data, setData] = useState<DataPerseveranceColored | null>(null);

  const [settingsCommon, setSettingsCommon] = useState(defaultSettingsCommon);
  const [settingsCOVA, setSettingsCOVA] = useState(defaultSettingsCOVA);
  const [settingsANGEL, setSettingsANGEL] = useState(defaultSettingsANGEL);

  const colorPreservation = () => {};

  const fetchData = async (algorithm: Algorithm) => {
    const updateData = (newData: DataPerseveranceLabelled) => {
      setData(() => {
        const colors = getColors(newData.labels, settingsCommon.dataPreservation, newData.prevPartsave);
        return {
          ...newData,
          points: newData.points.map((p) => p.map((p2) => p2 * 100) as Point2D | Point3D),
          colors,
        };
      });
    };

    let newData;
    if (algorithm === Algorithm.COVA) {
      const params: ParamsCOVA = {
        neighbourNumber: NEIGHBOUR_MARKS_ARR[settingsCommon.neighbour],
        lambdaParam: settingsCommon.lambda,
        alpha: settingsCOVA.alpha,
        isCohortNumberOriginal: settingsCOVA.c === C.ORIGINAL,
      };
      newData = await getDataCOVA(1, params);
      updateData(newData);
    } else if (algorithm === Algorithm.ANGEL) {
      // call angel endpoint init
      // while loop call angel dynamic function
    } else {
      // handle error
    }
  };

  // on change - fetch data
  useEffect(() => {
    fetchData(Algorithm.COVA);
  }, [settingsCommon, settingsCOVA, settingsANGEL]);

  return (
    <div className={classes.index}>
      <Settings
        {...{ settingsCommon, setSettingsCommon, settingsCOVA, setSettingsCOVA, settingsANGEL, setSettingsANGEL }}
      />
      {data && (
        <Visualization2D
          data={data}
          showPreservation={settingsCommon.dataPreservation === DataPreservation.ON}
          colorPreservation={colorPreservation}
        />
      )}
    </div>
  );
};

export default Examples;
