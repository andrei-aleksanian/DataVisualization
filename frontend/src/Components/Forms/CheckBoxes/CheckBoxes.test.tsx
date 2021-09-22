import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

import CheckBoxes, { CheckBoxesProps } from './CheckBoxes';

enum TestEntries {
  BOX1,
  BOX2,
}
let state = TestEntries.BOX1;
const setState = (event: React.ChangeEvent, currentValue: number) => {
  event.preventDefault();
  state = currentValue;
};
const testCheckBoxesProps: CheckBoxesProps = {
  entries: [
    { value: TestEntries.BOX1, text: 'box1' },
    { value: TestEntries.BOX2, text: 'box2' },
  ],
  currentValue: state,
  onChange: setState,
  labelText: 'Test Checkboxes',
};

const cleanupState = () => {
  state = TestEntries.BOX1;
};

const init = () => {
  render(<CheckBoxes {...testCheckBoxesProps} />);
};

describe('Test UI renders', () => {
  test('Settings matches snapshot', async () => {
    const { asFragment } = render(<CheckBoxes {...testCheckBoxesProps} />);
    expect(asFragment()).toMatchSnapshot();
  });

  test('Heading is rendered', () => {
    init();
    expect(screen.getByText(testCheckBoxesProps.labelText)).toBeInTheDocument();
  });

  test('Test all entries from entries array render', () => {
    init();
    for (let i = 0; i < testCheckBoxesProps.entries.length; i += 1) {
      const radio = screen.getByRole('radio', { name: testCheckBoxesProps.entries[i].text });
      expect(radio).toBeInTheDocument();
    }
  });
});

describe('Test UI changes and events', () => {
  test('Test click on a checkbox changes outside state', () => {
    init();
    const checkBox = screen.getByRole('radio', { name: testCheckBoxesProps.entries[1].text });
    userEvent.click(checkBox);

    expect(state).toBe(TestEntries.BOX2);
    cleanupState();
  });
});
