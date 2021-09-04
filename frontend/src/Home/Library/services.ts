import axios from 'utils/axios';
import { ExampleProps } from 'types/Examples';

const fetchExamples = async () => {
  const { data } = await axios.get('/examples');
  return data as ExampleProps[];
};

export default fetchExamples;
