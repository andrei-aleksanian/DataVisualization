import axios from './axios';
import { DATA, DataLabelled } from '../types/Data';
import { DataPerseverance, DATA_PERSEVERANCE } from '../types/Data/DataPerseverance';

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

export const getCovaDemo2 = async () => {
  try {
    const { data }: { data: DataPerseverance } = await axios.get('/cova-demo-perseverance');
    return data;
  } catch (e) {
    // eslint-disable-next-line no-console
    console.log(e);
    // todo: return error and handle it
    return DATA_PERSEVERANCE;
  }
};
