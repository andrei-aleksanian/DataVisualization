import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import userEvent from '@testing-library/user-event';

import Settings, {
  TEXT_CHECKBOX_ALGORITHM,
  TEXT_CHECKBOX_PRESERVATION,
  TEXT_SLIDER_LAMBDA,
  TEXT_SLIDER_NEIGHBOUR,
  TEXT_CHECKBOX_ANGEL,
  TEXT_CHECKBOX_COVA,
} from './Settings';
import { TEXT_CHECKBOX_C, TEXT_SLIDER_ALPHA } from './components/COVA';
import { TEXT_SLIDER_SPARSITY, TEXT_CHECKBOX_FLAG_MOVE, TEXT_SLIDER_EPSILON } from './components/ANGEL';

test('Settings matches snapshot', async () => {
  const { asFragment } = render(<Settings />, { wrapper: MemoryRouter });
  expect(asFragment()).toMatchSnapshot();
});

describe('Test UI changes and events', () => {
  beforeEach(() => {
    render(<Settings />, { wrapper: MemoryRouter });
  });

  test("Checkboxes clikcks don't change common attributes", () => {
    const checkCommonArttributes = () => {
      expect(screen.getByText(TEXT_CHECKBOX_ALGORITHM)).toBeInTheDocument();
      expect(screen.getByText(TEXT_SLIDER_NEIGHBOUR)).toBeInTheDocument();
      expect(screen.getByText(TEXT_SLIDER_LAMBDA)).toBeInTheDocument();
      expect(screen.getByText(TEXT_CHECKBOX_PRESERVATION)).toBeInTheDocument();
    };
    userEvent.click(screen.getByRole('radio', { name: TEXT_CHECKBOX_ANGEL }));
    checkCommonArttributes();

    userEvent.click(screen.getByRole('radio', { name: TEXT_CHECKBOX_COVA }));
    checkCommonArttributes();
  });

  test('Checkboxes ANGEL/COVA change the controls to ANGEL', async () => {
    userEvent.click(screen.getByRole('radio', { name: TEXT_CHECKBOX_ANGEL }));
    expect(screen.getByRole('radio', { name: TEXT_CHECKBOX_COVA })).not.toBeChecked();
    expect(screen.getByRole('radio', { name: TEXT_CHECKBOX_ANGEL })).toBeChecked();

    // ANGEL Elements should be rendered
    expect(screen.getByText(TEXT_SLIDER_SPARSITY)).toBeInTheDocument();
    expect(screen.getByText(TEXT_SLIDER_EPSILON)).toBeInTheDocument();
    expect(screen.getByText(TEXT_CHECKBOX_FLAG_MOVE)).toBeInTheDocument();

    // COVA elements shouldn't be rendered
    expect(screen.queryByText(TEXT_SLIDER_ALPHA)).not.toBeInTheDocument();
    expect(screen.queryByText(TEXT_CHECKBOX_C)).not.toBeInTheDocument();
  });

  test('Checkboxes ANGEL/COVA change the controls back to COVA', async () => {
    userEvent.click(screen.getByRole('radio', { name: TEXT_CHECKBOX_COVA }));
    expect(screen.getByRole('radio', { name: TEXT_CHECKBOX_ANGEL })).not.toBeChecked();
    expect(screen.getByRole('radio', { name: TEXT_CHECKBOX_COVA })).toBeChecked();

    // COVA Elements should be rendered
    expect(screen.getByText(TEXT_SLIDER_ALPHA)).toBeInTheDocument();
    expect(screen.getByText(TEXT_CHECKBOX_C)).toBeInTheDocument();

    // ANGEL elements shouldn't be rendered
    expect(screen.queryByText(TEXT_SLIDER_SPARSITY)).not.toBeInTheDocument();
    expect(screen.queryByText(TEXT_SLIDER_EPSILON)).not.toBeInTheDocument();
    expect(screen.queryByText(TEXT_CHECKBOX_FLAG_MOVE)).not.toBeInTheDocument();
  });
});
