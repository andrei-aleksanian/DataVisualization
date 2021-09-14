import { useState } from 'react';
import { useHistory } from 'react-router-dom';
import { DataPerseveranceLabelled, DataPerseveranceColored } from 'types/Data/DataPerseverance';
import { Popup } from 'Components/UI';
import { ParamsANGEL, ParamsCOVA } from 'types/Data/Params';
import { Algorithm } from 'types/Settings';
import { Point2D, Point3D } from 'types/Data';
import getColors from 'utils/getColors';
import { Dimension, SettingsCustom } from 'Home/Settings/components/Custom';
import Settings, {
  defaultSettingsCOVA,
  defaultSettingsANGEL,
  defaultSettingsCommon,
  NEIGHBOUR_MARKS_ARR,
  DataPreservation,
  CohortNumber,
  AnchorModification,
} from '../Settings';
import Visualization2D from '../Visualization2D';

import { getCovaDynamicInit, getCovaDynamic } from './services';

import classes from './Custom.module.scss';

export const defaultSettingsCustom: SettingsCustom = {
  file: null,
  dimension: Dimension.D2,
  validation: {
    validation: false,
  },
};

const Custom = () => {
  const [data, setData] = useState<DataPerseveranceColored | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [settingsCommon, setSettingsCommon] = useState(defaultSettingsCommon);
  const [settingsCOVA, setSettingsCOVA] = useState(defaultSettingsCOVA);
  const [settingsANGEL, setSettingsANGEL] = useState(defaultSettingsANGEL);
  const [settingsCustom, setSettingsCustom] = useState(defaultSettingsCustom);

  const history = useHistory();

  const updateData = (newData: DataPerseveranceLabelled) => {
    setData(() => {
      const colors = getColors(newData.labels);
      return {
        ...newData,
        points: newData.points.map((p) => p.map((p2) => p2 * 100) as Point2D | Point3D),
        colors,
      };
    });
  };

  const onSubmit = async () => {
    setSettingsCustom((prev) => ({ ...prev, validation: { validation: settingsCustom.file === null } }));
    if (settingsCustom.file === null) return;

    let newData: DataPerseveranceLabelled;
    if (settingsCommon.algorithm === Algorithm.COVA) {
      const params: ParamsCOVA = {
        neighbourNumber: NEIGHBOUR_MARKS_ARR[settingsCommon.neighbour],
        alpha: settingsCOVA.alpha,
        isCohortNumberOriginal: settingsCOVA.cohortNumber === CohortNumber.ORIGINAL,
      };
      newData = await getCovaDynamicInit(params, settingsCustom.file, settingsCustom.dimension);
      updateData(newData);
      while (newData.iteration < newData.maxIteration) {
        newData = await getCovaDynamic(newData); // eslint-disable-line
        updateData(newData);
      }
    } else {
      const params: ParamsANGEL = {
        neighbourNumber: NEIGHBOUR_MARKS_ARR[settingsCommon.neighbour],
        anchorDensity: settingsANGEL.anchorDensity,
        epsilon: settingsANGEL.epsilon,
        isAnchorModification: settingsANGEL.anchorModification === AnchorModification.ON,
      };
      console.log(params, settingsCustom.file); // eslint-disable-line no-console
    }
  };

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
          backLink: '/',
          customDataPage: {
            onSubmit,
            settingsCustom,
            setSettingsCustom,
          },
          reviewer: false,
          name: 'Custom Data',
        }}
      />
      {data && (
        <Visualization2D data={data} showPreservation={settingsCommon.dataPreservation === DataPreservation.ON} />
      )}
      {error && (
        <Popup
          onClick={() => {
            setError(null);
            history.push('/examples');
          }}
        />
      )}
    </div>
  );
};

export default Custom;
