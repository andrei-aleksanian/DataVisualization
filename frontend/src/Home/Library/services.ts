import axios from 'utils/axios';
import { ExampleProps } from 'types/Examples';
import tryPromise from 'utils/tryPromise';

const fetchExamples = async () => {
  const getExamples = async () => {
    const { data } = await axios.get('/examples');
    return data;
  };
  return tryPromise<ExampleProps[]>(getExamples);
};

export default fetchExamples;
