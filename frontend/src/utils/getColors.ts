export const COLOR_SCHEME = [
  '#fe5f55',
  '#235789',
  '#f1d302',
  '#161925',
  '#7e1f86',
  '#E0CBA8',
  '#f75c03',
  '#ff8cc6',
  '#419d78',
  '#4c212a',
];

const getRandomColor = (colorNum: number, colorsTotal = 1): string => {
  return `hsl(${(colorNum * (360 / colorsTotal) + 200) % 360},100%,50%)`;
};

const findUniqueColors = (uniqueLabels: number[]) => {
  const colors: string[] = [];

  for (let i = 0; i < uniqueLabels.length; i += 1) {
    const color = getRandomColor(i, uniqueLabels.length);
    colors.push(color);
  }

  const colorMap = Object.assign({}, ...Array.from(uniqueLabels, (value, i) => ({ [value]: colors[i] })));

  return colorMap;
};

const getUniqueLabels = (labels: number[]) => {
  const colorArr = new Set<number>();

  for (let i = 0; i < labels.length; i += 1) {
    colorArr.add(labels[i]);
  }

  return Array.from(colorArr);
};

export default (labels: number[]): string[] => {
  const colors: string[] = [];
  const uniqueLabels = getUniqueLabels(labels);
  let colorMap = null;
  if (uniqueLabels.length > 10) colorMap = findUniqueColors(uniqueLabels);

  for (let i = 0; i < labels.length; i += 1) {
    if (colorMap) colors.push(colorMap[labels[i]]);
    else colors.push(COLOR_SCHEME[labels[i]]);
  }

  return colors;
};
