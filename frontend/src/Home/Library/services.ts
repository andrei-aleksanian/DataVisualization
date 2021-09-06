import axios from 'utils/axios';
import { ExampleProps } from 'types/Examples';

const fetchExamples = async () => {
  try {
    const { data }: { data: ExampleProps[] } = await axios.get('/examples');
    return [data, null];
  } catch (error) {
    return [null, error];
  }
};

export default fetchExamples;
