import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

import Slider, { SliderProps } from './Slider';
import toMarks from './utils';

let state = 0;
const setState = (value: number) => {
  state = value;
};

const getSliderProps = (num: boolean = true): SliderProps => {
  const testSliderProps: SliderProps = {
    onChange: setState,
    min: 0,
    max: 0.3,
    step: 0.1,
    marksArr: [],
    text: 'Test Description',
    value: state,
  };
  if (num) {
    testSliderProps.marksArr = [0, 0.1, 0.2, 0.3];
  } else {
    testSliderProps.marksArr = ['0', '0.1', '0.2', '0.3'];
  }
  return testSliderProps;
};
const cleanupState = () => {
  state = 0;
};

const init = () => {
  render(<Slider {...getSliderProps()} />);
};

describe('Test Slider Component with marks number inputs', () => {
  test('Matches snapshot', async () => {
    const { asFragment } = render(<Slider {...getSliderProps()} />);
    expect(asFragment()).toMatchSnapshot();
  });

  test('Description is rendered', () => {
    init();
    expect(screen.getByText(getSliderProps().text)).toBeInTheDocument();
  });

  test('Change state on click', () => {
    init();
    userEvent.click(screen.getByText('0.1'));
    expect(state).toBe(0.1);
    userEvent.click(screen.getByText('0.2'));
    expect(state).toBe(0.2);

    cleanupState();
  });
});

describe('Test Slider Utils', () => {
  const style = {
    color: 'red',
  };

  test('toMarks converts number array correctly', () => {
    const marksArr = [0, 1, 2, 3];
    const marksObj = toMarks(marksArr, style);
    for (let i = 0; i < marksArr.length; i += 1) {
      const mark = marksArr[i];
      expect(marksObj[mark].label).toBe(mark);
      expect(marksObj[mark].style).toBe(style);
    }
  });

  test('toMarks converts string array correctly', () => {
    const marksArr = ['0', '1', '2', '3'];
    const marksObj = toMarks(marksArr, style);
    for (let i = 0; i < marksArr.length; i += 1) {
      const mark = marksArr[i];
      expect(marksObj[i].label).toBe(mark);
      expect(marksObj[i].style).toBe(style);
    }
  });
});
