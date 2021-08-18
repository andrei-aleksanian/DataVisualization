export default (data: number[]) => {
  /*
  Converts data like [1,2,3] to {1:1, 2:2, 3:3}
  */
  const obj = data.map((number) => [number, number]);
  return Object.fromEntries(obj);
};
