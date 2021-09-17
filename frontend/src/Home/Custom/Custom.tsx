import { useState } from 'react';
import { useHistory } from 'react-router-dom';
import { DataPerseveranceLabelled, DataPerseveranceColored } from 'types/Data/DataPerseverance';
import { Popup } from 'Components/UI';
import { ParamsANGEL, ParamsCOVA } from 'types/Data/Params';
import { Algorithm } from 'types/Settings';
import { Point2D, Point3D } from 'types/Data';
import getColors from 'utils/getColors';
import Settings, {
  defaultSettingsCOVA,
  defaultSettingsANGEL,
  defaultSettingsCommon,
  defaultSettingsCustom,
  NEIGHBOUR_MARKS_ARR,
  DataPreservation,
  CohortNumber,
  AnchorModification,
} from '../Settings';
import Visualization2D from '../Visualization2D';

import { getCovaDynamicInit, getCovaDynamic, getAngelDynamic, getAngelDynamicInit } from './services';

import classes from './Custom.module.scss';

// .mat files accepted only for this page
const ACCEPTED_TYPE = '.mat';
export const FILE_NULL = 'Please, provide a .mat file.';

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

  const validateFile = (file: File | null) => {
    /**
     * Validates file:
     * False - file invalid, True - valid.
     */
    const errorNew = file === null ? FILE_NULL : null;
    setSettingsCustom((prev) => ({ ...prev, file: { ...prev.file, error: errorNew } }));
    return !errorNew;
  };

  const onSubmit = async () => {
    if (!validateFile(settingsCustom.file.file)) return;
    const file = settingsCustom.file.file as File;

    let newData: DataPerseveranceLabelled;
    if (settingsCommon.algorithm === Algorithm.COVA) {
      const params: ParamsCOVA = {
        neighbourNumber: NEIGHBOUR_MARKS_ARR[settingsCommon.neighbour],
        alpha: settingsCOVA.alpha,
        isCohortNumberOriginal: settingsCOVA.cohortNumber === CohortNumber.ORIGINAL,
      };
      newData = await getCovaDynamicInit(params, file, settingsCustom.dimension);
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
      newData = await getAngelDynamicInit(params, file, settingsCustom.dimension);
      updateData(newData);
      while (newData.iteration < newData.maxIteration) {
        newData = await getAngelDynamic(newData); // eslint-disable-line
        updateData(newData);
      }
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
            error,
            acceptedType: ACCEPTED_TYPE,
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
