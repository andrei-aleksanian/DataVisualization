import { useState, useEffect } from 'react';
import { useHistory, useParams } from 'react-router-dom';

import getColors from 'utils/getColors';
import { Algorithm } from 'types/Settings';
import { Point2D, Point3D } from 'types/Data';
import { DataPerseveranceLabelled, DataPerseveranceColored } from 'types/Data/DataPerseverance';
import { ParamsANGEL, ParamsCOVA } from 'types/Data/Params';
import { Popup } from 'Components/UI';
import useDocumentTitle from 'hooks/useDocumentTitle';
import { getDataANGEL, getDataCOVA, getDataOriginal } from './services';

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

export const PAGE_TITLE = 'Example';
export interface ExampleProps {
  reviewer: boolean;
  backLink: string;
}

const Examples = ({ reviewer, backLink }: ExampleProps) => {
  const [data, setData] = useState<DataPerseveranceColored | null>(null);
  const [name, setName] = useState('');
  const [error, setError] = useState<string | null>(null);

  const [settingsCommon, setSettingsCommon] = useState(defaultSettingsCommon);
  const [settingsCOVA, setSettingsCOVA] = useState(defaultSettingsCOVA);
  const [settingsANGEL, setSettingsANGEL] = useState(defaultSettingsANGEL);

  const [isViewReset, setIsViewReset] = useState(false);

  const history = useHistory();
  const { id } = useParams<{ id: string }>();

  const updateData = (newData: DataPerseveranceLabelled, newName: string) => {
    setData(() => {
      const colors = getColors(newData.labels);
      return {
        ...newData,
        points: newData.points.map((p) => p.map((p2) => p2 * 100) as Point2D | Point3D),
        colors,
      };
    });
    setName(newName);
  };

  const fetchData = async (algorithm: Algorithm) => {
    let newData;
    if (algorithm === Algorithm.COVA) {
      const params: ParamsCOVA = {
        neighbourNumber: NEIGHBOUR_MARKS_ARR[settingsCommon.neighbour],
        alpha: settingsCOVA.alpha,
        isCohortNumberOriginal: settingsCOVA.cohortNumber === CohortNumber.ORIGINAL,
      };
      newData = await getDataCOVA(id, params);
    } else if (algorithm === Algorithm.ANGEL) {
      const params: ParamsANGEL = {
        neighbourNumber: NEIGHBOUR_MARKS_ARR[settingsCommon.neighbour],
        anchorDensity: settingsANGEL.anchorDensity,
        epsilon: settingsANGEL.epsilon,
        isAnchorModification: settingsANGEL.anchorModification === AnchorModification.ON,
      };
      newData = await getDataANGEL(id, params);
    } else {
      newData = await getDataOriginal(id);
    }
    return newData;
  };

  useEffect(() => {
    let isActive = true;

    const asyncHelper = async () => {
      const [newData, newError] = await fetchData(settingsCommon.algorithm);
      if (!isActive) return; // don't do anything if not rendered
      if (newData) updateData(newData.data, newData.name); // only update if  data is not null
      setError(newError); // always update error
    };

    asyncHelper();
    return () => {
      isActive = false;
    };
  }, [settingsCommon, settingsCOVA, settingsANGEL]);

  useDocumentTitle(`${PAGE_TITLE} ${name}`);
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
          setIsViewReset,
          backLink,
          reviewer,
          name: `Example: ${name}`,
        }}
      />
      {data && (
        <Visualization2D
          data={data}
          showPreservation={settingsCommon.dataPreservation === DataPreservation.ON}
          isViewReset={isViewReset}
        />
      )}
      {error && (
        <Popup
          onClick={() => {
            setError(null);
            history.push(backLink);
          }}
        />
      )}
    </div>
  );
};

export default Examples;
