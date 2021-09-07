const getRandomColor = (colorNum: number, colorsTotal = 1): string => {
  return `hsl(${(colorNum * (360 / colorsTotal) + 200) % 360},100%,50%)`;
};

const findUniqueColors = (labels: number[]) => {
  const colors: string[] = [];
  const colorArr = new Set<number>();

  for (let i = 0; i < labels.length; i += 1) {
    colorArr.add(labels[i]);
  }

  const reducedLabels = Array.from(colorArr);

  for (let i = 0; i < reducedLabels.length; i += 1) {
    const color = getRandomColor(i, reducedLabels.length);
    colors.push(color);
  }

  const colorMap = Object.assign({}, ...Array.from(reducedLabels, (value, i) => ({ [value]: colors[i] })));

  return colorMap;
};

export default (labels: number[]): string[] => {
  const colors: string[] = [];

  const colorMap = findUniqueColors(labels);

  for (let i = 0; i < labels.length; i += 1) {
    colors.push(colorMap[labels[i]]);
  }

  return colors;
};
