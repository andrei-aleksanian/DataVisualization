export type Response<T> = [T, null] | [null, string];

export const NETWORK_ERROR = "For some reason we can't access the server at this time. Please, try again later.";
export default async function tryPromise<T>(fun: () => Promise<T>): Promise<Response<T>> {
  try {
    const data = await fun();
    return [data, null];
  } catch (error) {
    let message = '';
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      message = error.response.data.detail;
    } else if (error.request) {
      // The request was made but no response was received
      // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
      // http.ClientRequest in node.js
      message = NETWORK_ERROR;
    } else {
      // Something happened in setting up the request that triggered an Error
      message = error.message;
    }
    return [null, message];
  }
}
