import axios from 'utils/axios';
import { DataPerseveranceLabelled, DataPerseveranceNamed } from 'types/Data/DataPerseverance';
import { ParamsANGEL, ParamsCOVA } from 'types/Data/Params';

export const getDataCOVA = async (exampleId: string, params: ParamsCOVA) => {
  try {
    const { data }: { data: { jsonData: string; exampleName: string } } = await axios.post(
      `/examples/cova/data/get/${exampleId}`,
      params
    );

    const dataParsed = JSON.parse(data.jsonData) as DataPerseveranceLabelled;
    const namedData: DataPerseveranceNamed = {
      data: dataParsed,
      name: data.exampleName,
    };
    return [namedData, null];
  } catch (error) {
    return [null, error];
  }
};

export const getDataANGEL = async (exampleId: string, params: ParamsANGEL) => {
  try {
    const { data }: { data: { jsonData: string; exampleName: string } } = await axios.post(
      `/examples/angel/data/get/${exampleId}`,
      params
    );

    const dataParsed = JSON.parse(data.jsonData) as DataPerseveranceLabelled;
    const namedData: DataPerseveranceNamed = {
      data: dataParsed,
      name: data.exampleName,
    };
    return [namedData, null];
  } catch (error) {
    return [null, error];
  }
};
