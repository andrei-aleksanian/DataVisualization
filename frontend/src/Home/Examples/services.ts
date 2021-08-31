import axios from 'utils/axios';
import { DataPerseveranceLabelled, DATA_PERSEVERANCE } from 'types/Data/DataPerseverance';
import { ParamsCOVA } from 'types/Data/Params';

export const getDataCOVA = async (exampleId: number, params: ParamsCOVA) => {
  try {
    // TODO change this string to something else
    const { data }: { data: string | DataPerseveranceLabelled } = await axios.post(
      `/examples/cova/data/get/${exampleId}`,
      params
    );

    if (typeof data === 'string') return JSON.parse(data) as DataPerseveranceLabelled;
    return data;
  } catch (e) {
    // eslint-disable-next-line no-console
    console.log(e);
    // todo: return error and handle it
    return DATA_PERSEVERANCE;
  }
};

export const getDataANGEL = async (exampleId: number) => {
  try {
    const { data }: { data: DataPerseveranceLabelled } = await axios.get(`/examples/angel/data/get/${exampleId}`);
    return data;
  } catch (e) {
    // eslint-disable-next-line no-console
    console.log(e);
    // todo: return error and handle it
    return DATA_PERSEVERANCE;
  }
};
