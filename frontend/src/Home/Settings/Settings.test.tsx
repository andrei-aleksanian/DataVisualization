import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';

import { Algorithm } from 'types/Settings';
import Settings, {
  TEXT_CHECKBOX_ALGORITHM,
  TEXT_CHECKBOX_PRESERVATION,
  TEXT_SLIDER_NEIGHBOUR,
  TEXT_CHECKBOX_ANGEL,
  TEXT_CHECKBOX_COVA,
  defaultSettingsCommon,
  SettingsProps,
} from './Settings';
import { TEXT_CHECKBOX_COHORT_NUMBER, TEXT_SLIDER_ALPHA, defaultSettingsCOVA } from './components/COVA';
import {
  TEXT_SLIDER_ANCHOR_DENSITY,
  TEXT_CHECKBOX_ANCHOR_MODIFICATION,
  TEXT_SLIDER_EPSILON,
  defaultSettingsANGEL,
} from './components/ANGEL';

const mockSettingsProps: SettingsProps = {
  settingsCommon: defaultSettingsCommon,
  setSettingsCommon: () => {},
  settingsCOVA: defaultSettingsCOVA,
  setSettingsCOVA: () => {},
  settingsANGEL: defaultSettingsANGEL,
  setSettingsANGEL: () => {},
  backLink: '/examples',
};

test('Settings matches snapshot', () => {
  const { asFragment } = render(<Settings {...mockSettingsProps} />, { wrapper: MemoryRouter });
  expect(asFragment()).toMatchSnapshot();
});

describe('Test UI changes and events', () => {
  const init = (algorithm: Algorithm) => {
    const mockSettingsPropsInit: SettingsProps = {
      ...mockSettingsProps,
      settingsCommon: {
        ...mockSettingsProps.settingsCommon,
        algorithm, // pretending we clicked the button in parent
      },
    };
    render(<Settings {...mockSettingsPropsInit} />, { wrapper: MemoryRouter });
  };

  const checkCommonArttributes = () => {
    expect(screen.getByText(TEXT_CHECKBOX_ALGORITHM)).toBeInTheDocument();
    expect(screen.getByText(TEXT_SLIDER_NEIGHBOUR)).toBeInTheDocument();
    expect(screen.getByText(TEXT_CHECKBOX_PRESERVATION)).toBeInTheDocument();
  };

  test("Checkboxes clicks don't change common attributes", () => {
    init(Algorithm.ANGEL);
    checkCommonArttributes();
  });

  test("Checkboxes clicks don't change common attributes", () => {
    init(Algorithm.COVA);
    checkCommonArttributes();
  });

  test('Checkboxes ANGEL/COVA change the controls to ANGEL', () => {
    init(Algorithm.ANGEL);

    expect(screen.getByRole('radio', { name: TEXT_CHECKBOX_COVA })).not.toBeChecked();
    expect(screen.getByRole('radio', { name: TEXT_CHECKBOX_ANGEL })).toBeChecked();

    // ANGEL Elements should be rendered
    expect(screen.getByText(TEXT_SLIDER_ANCHOR_DENSITY)).toBeInTheDocument();
    expect(screen.getByText(TEXT_SLIDER_EPSILON)).toBeInTheDocument();
    expect(screen.getByText(TEXT_CHECKBOX_ANCHOR_MODIFICATION)).toBeInTheDocument();

    // COVA elements shouldn't be rendered
    expect(screen.queryByText(TEXT_SLIDER_ALPHA)).not.toBeInTheDocument();
    expect(screen.queryByText(TEXT_CHECKBOX_COHORT_NUMBER)).not.toBeInTheDocument();
  });

  test('Checkboxes ANGEL/COVA change the controls back to COVA', async () => {
    init(Algorithm.COVA);

    expect(screen.getByRole('radio', { name: TEXT_CHECKBOX_ANGEL })).not.toBeChecked();
    expect(screen.getByRole('radio', { name: TEXT_CHECKBOX_COVA })).toBeChecked();

    // COVA Elements should be rendered
    expect(screen.getByText(TEXT_SLIDER_ALPHA)).toBeInTheDocument();
    expect(screen.getByText(TEXT_CHECKBOX_COHORT_NUMBER)).toBeInTheDocument();

    // ANGEL elements shouldn't be rendered
    expect(screen.queryByText(TEXT_SLIDER_ANCHOR_DENSITY)).not.toBeInTheDocument();
    expect(screen.queryByText(TEXT_SLIDER_EPSILON)).not.toBeInTheDocument();
    expect(screen.queryByText(TEXT_CHECKBOX_ANCHOR_MODIFICATION)).not.toBeInTheDocument();
  });
});
