import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';

import { Algorithm } from 'types/Settings';
import { DATA_TESTID_MODAL } from 'Components/UI';
import Settings, {
  TEXT_CHECKBOX_ALGORITHM,
  TEXT_CHECKBOX_PRESERVATION,
  TEXT_SLIDER_NEIGHBOUR,
  TEXT_CHECKBOX_ANGEL,
  TEXT_CHECKBOX_COVA,
  TEXT_CHECKBOX_ORIGINAL,
  defaultSettingsCommon,
  SettingsProps,
} from '.';
import { TEXT_CHECKBOX_COHORT_NUMBER, TEXT_SLIDER_ALPHA, defaultSettingsCOVA } from './components/COVA';
import {
  TEXT_SLIDER_ANCHOR_DENSITY,
  TEXT_CHECKBOX_ANCHOR_MODIFICATION,
  TEXT_SLIDER_EPSILON,
  defaultSettingsANGEL,
} from './components/ANGEL';
import { defaultSettingsCustom } from './components/Custom';

const mockSettingsProps: SettingsProps = {
  settingsCommon: defaultSettingsCommon,
  setSettingsCommon: () => {},
  settingsCOVA: defaultSettingsCOVA,
  setSettingsCOVA: () => {},
  settingsANGEL: defaultSettingsANGEL,
  setSettingsANGEL: () => {},
  backLink: '/examples',
  reviewer: false,
  name: 'test',
};

const getSettingsProps = (reviewer: boolean = false): SettingsProps => {
  const props: SettingsProps = reviewer
    ? {
        ...mockSettingsProps,
        customDataPage: {
          setSettingsCustom: () => {},
          settingsCustom: defaultSettingsCustom,
          acceptedType: '.mat',
        },
      }
    : {
        ...mockSettingsProps,
        reviewer: true,
      };
  return props;
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
    return render(<Settings {...mockSettingsPropsInit} />, { wrapper: MemoryRouter });
  };

  const checkCommonArttributes = (asFragment: () => DocumentFragment) => {
    expect(screen.getByText(TEXT_CHECKBOX_ALGORITHM)).toBeInTheDocument();
    expect(screen.getByText(TEXT_SLIDER_NEIGHBOUR)).toBeInTheDocument();
    expect(screen.getByText(TEXT_CHECKBOX_PRESERVATION)).toBeInTheDocument();
    expect(asFragment()).toMatchSnapshot();
  };

  test("Checkboxes clicks don't change common attributes", () => {
    const { asFragment } = init(Algorithm.ANGEL);
    checkCommonArttributes(asFragment);
  });

  test("Checkboxes clicks don't change common attributes", () => {
    const { asFragment } = init(Algorithm.COVA);
    checkCommonArttributes(asFragment);
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

  test('Checkboxes ANGEL/COVA change the controls to ORIGINAL', async () => {
    init(Algorithm.ORIGINAL);

    expect(screen.getByRole('radio', { name: TEXT_CHECKBOX_ANGEL })).not.toBeChecked();
    expect(screen.getByRole('radio', { name: TEXT_CHECKBOX_COVA })).not.toBeChecked();
    expect(screen.getByRole('radio', { name: TEXT_CHECKBOX_ORIGINAL })).toBeChecked();

    // Modal should be rendered above all controls
    expect(screen.getByTestId(DATA_TESTID_MODAL)).toBeInTheDocument();
  });
});

test('Settings for Custom page matches snapshot', () => {
  const { asFragment } = render(<Settings {...getSettingsProps()} />, { wrapper: MemoryRouter });
  expect(asFragment()).toMatchSnapshot();
});

test('Settings for Reviewer page matches snapshot', () => {
  const { asFragment } = render(<Settings {...getSettingsProps(true)} />, { wrapper: MemoryRouter });
  expect(asFragment()).toMatchSnapshot();
});
