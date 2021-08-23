import { CSSProperties, ReactNode } from 'react';

export interface Marks {
  [number: number]: { style: CSSProperties; label: ReactNode };
}

const toMarks = (data: (string | number)[], style: CSSProperties) => {
  /*
  Converts data like ['1','10%'] to:
  {0:{style: CSSProperties, label: 1}, 1:{style: CSSProperties, label: '10%'}} (0 and 1 are indexes of teh input array)
  and data like [1,2] to:
  {1:{style: CSSProperties, label: 1}, 2:{style: CSSProperties, label: 2}}

  Used in the Slider Component internally to allow ease of input in the parent components.
  */

  const marks: Marks = {};
  for (let i = 0; i < data.length; i += 1) {
    const currentMark = data[i];
    if (typeof currentMark === 'string') {
      marks[i] = {
        style,
        label: data[i],
      };
    } else {
      marks[currentMark] = {
        style,
        label: data[i],
      };
    }
  }

  return marks;
};

export default toMarks;
