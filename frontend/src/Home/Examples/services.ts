import axios from 'utils/axios';
import { DataPerseveranceLabelled } from 'types/Data/DataPerseverance';
import { ParamsANGEL, ParamsCOVA } from 'types/Data/Params';

export const getDataCOVA = async (exampleId: number, params: ParamsCOVA) => {
  try {
    const { data }: { data: string } = await axios.post(`/examples/cova/data/get/${exampleId}`, params);

    const dataParsed = JSON.parse(data) as DataPerseveranceLabelled;
    return [dataParsed, null];
  } catch (error) {
    return [null, error];
  }
};

export const getDataANGEL = async (exampleId: number, params: ParamsANGEL) => {
  try {
    const { data }: { data: string } = await axios.post(`/examples/angel/data/get/${exampleId}`, params);

    const dataParsed = JSON.parse(data) as DataPerseveranceLabelled;
    return [dataParsed, null];
  } catch (error) {
    return [null, error];
  }
};
