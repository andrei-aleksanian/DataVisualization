import axios from 'utils/axios';
import { ParamsCOVA } from 'types/Data/Params';
import { Dimension } from 'Home/Settings/components/Custom';
import { DataPerseveranceLabelled, DATA_PERSEVERANCE } from '../../types/Data/DataPerseverance';

export const getCovaDynamicInit = async (params: ParamsCOVA, file: File, dimension: Dimension) => {
  const formData = new FormData();
  formData.append('dimension', dimension === Dimension.D2 ? '2' : '3');
  formData.append('neighbourNumber', params.neighbourNumber);
  formData.append('lambdaParam', params.lambdaParam.toString());
  formData.append('alpha', params.alpha.toString());
  formData.append('isCohortNumberOriginal', params.isCohortNumberOriginal.toString());
  formData.append('file', file);

  try {
    const config = {
      headers: { 'content-type': 'multipart/form-data' },
    };
    const { data }: { data: DataPerseveranceLabelled } = await axios.post('/dynamic/cova', formData, config);
    return data;
  } catch (e) {
    // eslint-disable-next-line no-console
    console.log(e);
    // todo: return error and handle it
    return DATA_PERSEVERANCE;
  }
};

export const getCovaDynamic = async (body: DataPerseveranceLabelled) => {
  try {
    const { data }: { data: DataPerseveranceLabelled } = await axios.post('/cova-demo-dynamic', body);
    return data;
  } catch (e) {
    // eslint-disable-next-line no-console
    console.log(e);
    // todo: return error and handle it
    return DATA_PERSEVERANCE;
  }
};
