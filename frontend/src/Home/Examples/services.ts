import axios from 'utils/axios';
import { DataPerseveranceLabelled, DataPerseveranceNamed, DATA_PERSEVERANCE } from 'types/Data/DataPerseverance';
import { ParamsANGEL, ParamsCOVA } from 'types/Data/Params';
import tryPromise from 'utils/tryPromise';

export const getDataCOVA = async (exampleId: string, params: ParamsCOVA) => {
  const promise = async () => {
    const { data }: { data: { jsonData: string; exampleName: string } } = await axios.post(
      `/examples/cova/data/get/${exampleId}`,
      params
    );

    const dataParsed = JSON.parse(data.jsonData) as DataPerseveranceLabelled;
    const namedData: DataPerseveranceNamed = {
      data: dataParsed,
      name: data.exampleName,
    };
    return namedData;
  };
  return tryPromise(promise);
};

export const getDataANGEL = async (exampleId: string, params: ParamsANGEL) => {
  const promise = async () => {
    const { data }: { data: { jsonData: string; exampleName: string } } = await axios.post(
      `/examples/angel/data/get/${exampleId}`,
      params
    );

    const dataParsed = JSON.parse(data.jsonData) as DataPerseveranceLabelled;
    const namedData: DataPerseveranceNamed = {
      data: dataParsed,
      name: data.exampleName,
    };
    return namedData;
  };
  return tryPromise(promise);
};

export const getDataOriginal = async (exampleId: string) => {
  const promise = async () => {
    const { data }: { data: { originalData: string; labels: string; dimension2D: boolean; exampleName: string } } =
      await axios.get(`/examples/${exampleId}`);

    const originalData = JSON.parse(data.originalData);
    const labels = JSON.parse(data.labels);
    const namedData: DataPerseveranceNamed = {
      data: {
        ...DATA_PERSEVERANCE,
        points: originalData,
        labels,
        dimension2D: data.dimension2D,
      },
      name: data.exampleName,
    };
    return namedData;
  };
  return tryPromise(promise);
};
