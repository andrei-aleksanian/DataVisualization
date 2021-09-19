import axios from 'utils/axios';
import { ParamsCOVA, ParamsANGEL } from 'types/Data/Params';
import { Dimension } from 'Home/Settings/components/Custom';
import tryPromise from 'utils/tryPromise';
import { DataPerseveranceLabelled } from '../../types/Data/DataPerseverance';

export const getCovaDynamicInit = async (params: ParamsCOVA, file: File, dimension: Dimension) => {
  const promise = async () => {
    const formData = new FormData();
    formData.append('dimension', dimension === Dimension.D2 ? '2' : '3');
    formData.append('neighbourNumber', params.neighbourNumber);
    formData.append('alpha', params.alpha.toString());
    formData.append('isCohortNumberOriginal', params.isCohortNumberOriginal.toString());
    formData.append('file', file);

    const config = {
      headers: { 'content-type': 'multipart/form-data' },
    };
    return (await axios.post<DataPerseveranceLabelled>('/dynamic/cova-init', formData, config)).data;
  };

  return tryPromise(promise);
};

export const getCovaDynamic = async (body: DataPerseveranceLabelled) =>
  tryPromise(async () => (await axios.post<DataPerseveranceLabelled>('/dynamic/cova', body)).data);

export const getAngelDynamicInit = async (params: ParamsANGEL, file: File, dimension: Dimension) => {
  const promise = async () => {
    const formData = new FormData();
    formData.append('dimension', dimension === Dimension.D2 ? '2' : '3');
    formData.append('neighbourNumber', params.neighbourNumber);
    formData.append('anchorDensity', params.anchorDensity.toString());
    formData.append('epsilon', params.epsilon.toString());
    formData.append('isAnchorModification', params.isAnchorModification.toString());
    formData.append('file', file);

    const config = {
      headers: { 'content-type': 'multipart/form-data' },
    };
    const { data }: { data: DataPerseveranceLabelled } = await axios.post<DataPerseveranceLabelled>(
      '/dynamic/angel-init',
      formData,
      config
    );
    return data;
  };

  return tryPromise(promise);
};

export const getAngelDynamic = async (body: DataPerseveranceLabelled) =>
  tryPromise(async () => (await axios.post<DataPerseveranceLabelled>('/dynamic/angel', body)).data);
