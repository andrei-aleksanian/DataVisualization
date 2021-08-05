import axios from './utils/axios';
import { Data2D } from './types/Data';

export const getAngelDemo = async () => {
  const { data }: { data: Data2D } = await axios.get('/angel-demo');

  return data;
};

export const getCovaDemo = async () => {
  const { data }: { data: Data2D } = await axios.get('/cova-demo');

  return data;
};
