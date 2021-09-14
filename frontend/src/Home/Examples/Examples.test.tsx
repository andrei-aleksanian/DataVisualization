import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

import { MemoryRouter } from 'react-router-dom';
import axios from 'utils/axios';
import { DATA_PERSEVERANCE } from 'types/Data/DataPerseverance';
import { POPUP_TEXT } from 'Components/UI';
import Examples from '.';

export const defaultExamplesProps = {
  reviewer: false,
  backLink: '/examples',
};

export const mockData = { data: { jsonData: JSON.stringify(DATA_PERSEVERANCE), exampleName: 'Example' } };
const mockAxios = () => {
  return jest.spyOn(axios, 'post');
};

test('Examples matches snapshot', async () => {
  const mockedAxios = mockAxios();
  mockedAxios.mockResolvedValueOnce(mockData);

  const { asFragment } = await waitFor(async () =>
    render(<Examples {...defaultExamplesProps} />, { wrapper: MemoryRouter })
  );
  expect(asFragment()).toMatchSnapshot();
});

describe('Examples fetches data correctly', () => {
  test('Examples fetches data on render', async () => {
    const mockedAxios = mockAxios();
    mockedAxios.mockResolvedValueOnce({
      data: { jsonData: JSON.stringify(DATA_PERSEVERANCE), exampleName: 'Example' },
    });

    await waitFor(() => {
      render(<Examples {...defaultExamplesProps} />, { wrapper: MemoryRouter });
    });
    const canvas = await waitFor(() => screen.getByTestId('canvas'));
    const popup = await waitFor(() => screen.queryByText(POPUP_TEXT));

    expect(canvas).toBeInTheDocument();
    expect(mockedAxios).toHaveBeenCalledTimes(1);
    expect(popup).not.toBeInTheDocument();
  });

  test('Examples fetches data on click', async () => {
    const mockedAxios = mockAxios();
    mockedAxios.mockResolvedValueOnce(mockData);
    mockedAxios.mockResolvedValueOnce(mockData);

    await waitFor(() => {
      render(<Examples {...defaultExamplesProps} />, { wrapper: MemoryRouter });
    });

    await waitFor(() => {
      userEvent.click(screen.getByText('COVA'));
    });
    expect(mockedAxios).toHaveBeenCalledTimes(2);
  });

  test("Examples displays an error popup when the data can't be fetched", async () => {
    const mockedAxios = mockAxios();
    mockedAxios.mockRejectedValueOnce(new Error('Something went wrong'));

    await waitFor(async () => {
      render(<Examples {...defaultExamplesProps} />, { wrapper: MemoryRouter });
    });

    const popup = await waitFor(() => screen.getByText(POPUP_TEXT));
    expect(popup).toBeInTheDocument();
  });
});
