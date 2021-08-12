import axios from './axios';
import { DATA, DataLabelled } from '../types/Data';
import { DataPerseveranceLabelled, DATA_PERSEVERANCE } from '../types/Data/DataPerseverance';

export const getAngelDemo = async () => {
  try {
    const { data }: { data: DataLabelled } = await axios.get('/angel-demo');
    return data;
  } catch (e) {
    // eslint-disable-next-line no-console
    console.log(e);
    // todo: return error and handle it
    return DATA;
  }
};

export const getCovaDemo = async () => {
  try {
    const { data }: { data: DataLabelled } = await axios.get('/cova-demo');
    return data;
  } catch (e) {
    // eslint-disable-next-line no-console
    console.log(e);
    // todo: return error and handle it
    return DATA;
  }
};

export const getCovaDemo2Init = async () => {
  try {
    const { data }: { data: DataPerseveranceLabelled } = await axios.get('/cova-demo-dynamic');
    return data;
  } catch (e) {
    // eslint-disable-next-line no-console
    console.log(e);
    // todo: return error and handle it
    return DATA_PERSEVERANCE;
  }
};

export const getCovaDemo2 = async (iteration: number, body: DataPerseveranceLabelled) => {
  try {
    const { data }: { data: DataPerseveranceLabelled } = await axios.post('/cova-demo-dynamic', body);
    return data;
  } catch (e) {
    // eslint-disable-next-line no-console
    if (e.response !== undefined) console.log(e.response.data);
    else console.log(e);
    // todo: return error and handle it
    return DATA_PERSEVERANCE;
  }
};
