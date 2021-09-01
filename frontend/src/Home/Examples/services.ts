import axios from 'utils/axios';
import { DataPerseveranceLabelled, DATA_PERSEVERANCE } from 'types/Data/DataPerseverance';
import { ParamsANGEL, ParamsCOVA } from 'types/Data/Params';

export const getDataCOVA = async (exampleId: number, params: ParamsCOVA) => {
  try {
    // TODO change this string to something else
    const { data }: { data: string } = await axios.post(`/examples/cova/data/get/${exampleId}`, params);

    return JSON.parse(data) as DataPerseveranceLabelled;
  } catch (e) {
    // eslint-disable-next-line no-console
    console.log(e);
    // todo: return error and handle it
    return DATA_PERSEVERANCE;
  }
};

export const getDataANGEL = async (exampleId: number, params: ParamsANGEL) => {
  try {
    // TODO change this string to something else
    const { data }: { data: string } = await axios.post(`/examples/angel/data/get/${exampleId}`, params);

    return JSON.parse(data) as DataPerseveranceLabelled;
  } catch (e) {
    // eslint-disable-next-line no-console
    console.log(e);
    // todo: return error and handle it
    return DATA_PERSEVERANCE;
  }
};
