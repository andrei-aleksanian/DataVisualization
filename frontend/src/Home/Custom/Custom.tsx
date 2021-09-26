import { useState } from 'react';
import { DataPerseveranceLabelled, DataPerseveranceColored } from 'types/Data/DataPerseverance';
import { ParamsANGEL, ParamsCOVA } from 'types/Data/Params';
import { Algorithm } from 'types/Settings';
import { Point2D, Point3D } from 'types/Data';
import getColors from 'utils/getColors';
import { Response } from 'utils/tryPromise';
import useIsMounted from 'hooks/useIsMounted';
import useDocumentTitle from 'hooks/useDocumentTitle';
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

export const PAGE_TITLE = 'Custom Data';
// .mat files accepted only for this page
const ACCEPTED_TYPE = '.mat';
export const TEXT_FILE_NULL = 'Please, provide a .mat file.';

const Custom = () => {
  const [data, setData] = useState<DataPerseveranceColored | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const [settingsCommon, setSettingsCommon] = useState(defaultSettingsCommon);
  const [settingsCOVA, setSettingsCOVA] = useState(defaultSettingsCOVA);
  const [settingsANGEL, setSettingsANGEL] = useState(defaultSettingsANGEL);
  const [settingsCustom, setSettingsCustom] = useState(defaultSettingsCustom);

  const isActive = useIsMounted();

  const updateData = ([newData, newError]: Response<DataPerseveranceLabelled>): boolean => {
    setError(newError);
    if (!newData && newError) {
      return false;
    }
    setData(() => {
      const colors = getColors(newData!.labels);
      return {
        ...newData!,
        points: newData!.points.map((p) => p.map((p2) => p2 * 100) as Point2D | Point3D),
        colors,
      };
    });
    return true;
  };

  const validateFile = (file: File | null) => {
    /**
     * Validates file:
     * False - file invalid, True - valid.
     */
    const errorNew = file === null ? TEXT_FILE_NULL : null;
    setSettingsCustom((prev) => ({ ...prev, file: { ...prev.file, error: errorNew } }));
    return !errorNew;
  };

  const onSubmit = async () => {
    if (!validateFile(settingsCustom.file.file)) return;
    const file = settingsCustom.file.file as File;
    setError(null);
    setIsLoading(true);

    if (settingsCommon.algorithm === Algorithm.COVA) {
      const params: ParamsCOVA = {
        neighbourNumber: NEIGHBOUR_MARKS_ARR[settingsCommon.neighbour],
        alpha: settingsCOVA.alpha,
        isCohortNumberOriginal: settingsCOVA.cohortNumber === CohortNumber.ORIGINAL,
      };
      let res = await getCovaDynamicInit(params, file, settingsCustom.dimension);
      let [newData] = res;
      if (!isActive.current || !updateData(res)) {
        setIsLoading(false);
        return;
      }
      while (newData!.iteration < newData!.maxIteration) {
        res = await getCovaDynamic(newData!); // eslint-disable-line
        [newData] = res;
        if (!isActive.current || !updateData(res)) {
          setIsLoading(false);
          return;
        }
      }
    } else {
      const params: ParamsANGEL = {
        neighbourNumber: NEIGHBOUR_MARKS_ARR[settingsCommon.neighbour],
        anchorDensity: settingsANGEL.anchorDensity,
        epsilon: settingsANGEL.epsilon,
        isAnchorModification: settingsANGEL.anchorModification === AnchorModification.ON,
      };
      let res = await getAngelDynamicInit(params, file, settingsCustom.dimension);
      let [newData] = res;
      if (!isActive.current || !updateData(res)) {
        setIsLoading(false);
        return;
      }
      while (newData!.iteration < newData!.maxIteration) {
        res = await getAngelDynamic(newData!); // eslint-disable-line
        [newData] = res;
        if (!isActive.current || !updateData(res)) {
          setIsLoading(false);
          return;
        }
      }
    }
    setIsLoading(false);
  };

  useDocumentTitle(PAGE_TITLE);

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
            settingsCustom,
            setSettingsCustom,
            acceptedType: ACCEPTED_TYPE,
          },
          submitProps: {
            onSubmit,
            error,
          },
          reviewer: false,
          name: 'Custom Data',
          isLoading,
        }}
      />
      {data && (
        <Visualization2D
          data={data}
          showPreservation={settingsCommon.dataPreservation === DataPreservation.ON}
          isViewReset={false}
        />
      )}
    </div>
  );
};

export default Custom;
