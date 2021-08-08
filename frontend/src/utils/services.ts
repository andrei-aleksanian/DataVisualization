import axios from './axios';
import { DATA, Data2D } from '../types/Data';

export const getAngelDemo = async () => {
  try {
    const { data }: { data: Data2D } = await axios.get('/angel-demo');
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
    const { data }: { data: Data2D } = await axios.get('/cova-demo');
    return data;
  } catch (e) {
    // eslint-disable-next-line no-console
    console.log(e);
    // todo: return error and handle it
    return DATA;
  }
};
