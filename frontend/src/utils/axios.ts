import axios, { AxiosInstance } from 'axios';

const getInstance = (): AxiosInstance => {
  let baseURL = window.location.origin;
  // localhost:3000 is for development only
  // potential todo: change this to an env variable
  if (window.location.origin === 'http://localhost:3000') {
    baseURL = 'http://localhost:8080';
  }

  return axios.create({
    baseURL: `${baseURL}/api`,
  });
};

export default getInstance();
