import { useState, useEffect } from 'react';
import { useHistory, useParams } from 'react-router-dom';

import getColors from 'utils/getColors';
import { Algorithm } from 'types/Settings';
import { Point2D, Point3D } from 'types/Data';
import { DataPerseveranceLabelled, DataPerseveranceColored } from 'types/Data/DataPerseverance';
import { ParamsANGEL, ParamsCOVA } from 'types/Data/Params';
import { Popup } from 'Components/UI';
import { getDataANGEL, getDataCOVA } from './services';

import Settings, {
  defaultSettingsCOVA,
  defaultSettingsANGEL,
  defaultSettingsCommon,
  NEIGHBOUR_MARKS_ARR,
  CohortNumber,
  DataPreservation,
  AnchorModification,
} from '../Settings';
import Visualization2D from '../Visualization2D';

import classes from './Examples.module.scss';

export const POPUP_TEXT = 'Oops, something went wrong. Please try again later.';

const Examples = () => {
  const [data, setData] = useState<DataPerseveranceColored | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [settingsCommon, setSettingsCommon] = useState(defaultSettingsCommon);
  const [settingsCOVA, setSettingsCOVA] = useState(defaultSettingsCOVA);
  const [settingsANGEL, setSettingsANGEL] = useState(defaultSettingsANGEL);

  const history = useHistory();
  const { id } = useParams<{ id: string }>();

  const updateData = (newData: DataPerseveranceLabelled) => {
    setData(() => {
      const colors = getColors(newData.labels);
      return {
        ...newData,
        points: newData.points.map((p) => p.map((p2) => p2 * 100 - 50) as Point2D | Point3D),
        colors,
      };
    });
  };

  const fetchData = async (algorithm: Algorithm) => {
    let newData;
    if (algorithm === Algorithm.COVA) {
      const params: ParamsCOVA = {
        neighbourNumber: NEIGHBOUR_MARKS_ARR[settingsCommon.neighbour],
        lambdaParam: settingsCommon.lambda,
        alpha: settingsCOVA.alpha,
        isCohortNumberOriginal: settingsCOVA.cohortNumber === CohortNumber.ORIGINAL,
      };
      newData = await getDataCOVA(id, params);
    } else {
      const params: ParamsANGEL = {
        neighbourNumber: NEIGHBOUR_MARKS_ARR[settingsCommon.neighbour],
        lambdaParam: settingsCommon.lambda,
        anchorDensity: settingsANGEL.anchorDensity,
        epsilon: settingsANGEL.epsilon,
        isAnchorModification: settingsANGEL.anchorModification === AnchorModification.ON,
      };
      newData = await getDataANGEL(id, params);
    }
    return newData;
  };

  useEffect(() => {
    let isActive = true;

    const asyncHelper = async () => {
      const [newData, newError] = await fetchData(settingsCommon.algorithm);
      if (!isActive) return; // don't do anything if not rendered
      if (newData) updateData(newData); // only update if  data is not null
      setError(newError); // always update error
    };

    asyncHelper();
    return () => {
      isActive = false;
    };
  }, [settingsCommon, settingsCOVA, settingsANGEL]);

  return (
    <div className={classes.index}>
      <Settings
        {...{
          settingsCommon,
          setSettingsCommon,
          settingsCOVA,
          setSettingsCOVA,
          settingsANGEL,
          setSettingsANGEL,
          backLink: '/examples',
        }}
      />
      {data && (
        <Visualization2D data={data} showPreservation={settingsCommon.dataPreservation === DataPreservation.ON} />
      )}
      {error && (
        <Popup
          text={POPUP_TEXT}
          onClick={() => {
            setError(null);
            history.push('/examples');
          }}
        />
      )}
    </div>
  );
};

export default Examples;
