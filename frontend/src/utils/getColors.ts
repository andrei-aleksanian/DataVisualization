export const COLOR_SCHEME = [
  '#fe5f55',
  '#fea82f',
  '#006d77',
  '#A2D729',
  '#FC6DAB',
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

const colorDefault = (labels: number[], uniqueLabels: number[]) => {
  const uniqueLabelsMap = {} as any; // should be something like {[number: number]}
  const colors = [];
  for (let i = 0; i < uniqueLabels.length; i += 1) {
    uniqueLabelsMap[uniqueLabels[i]] = i;
  }

  for (let i = 0; i < labels.length; i += 1) {
    colors.push(COLOR_SCHEME[uniqueLabelsMap[labels[i]]]);
  }
  return colors;
};

const colorByHSL = (labels: number[], uniqueLabels: number[]) => {
  const colorMap = findUniqueColors(uniqueLabels);
  const colors = [];
  for (let i = 0; i < labels.length; i += 1) {
    colors.push(colorMap[labels[i]]);
  }
  return colors;
};

export default (labels: number[]): string[] => {
  const uniqueLabels = getUniqueLabels(labels);

  return uniqueLabels.length < 10 ? colorDefault(labels, uniqueLabels) : colorByHSL(labels, uniqueLabels);
};
