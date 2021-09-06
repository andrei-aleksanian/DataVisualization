import { render, screen, waitFor } from '@testing-library/react';

import { MemoryRouter } from 'react-router-dom';
import { ExampleProps } from 'types/Examples';
import axios from 'utils/axios';
import Library, { TEXT_POPUP } from '.';

export const placeholderExamples: ExampleProps[] = [
  {
    id: 1,
    name: 'test',
    imagePath: 'test.jpg',
    description: 'description',
  },
];

export const mockAxios = () => {
  return jest.spyOn(axios, 'get');
};

test('Library matches snapshot', async () => {
  const mockedAxios = mockAxios();
  mockedAxios.mockResolvedValueOnce({ data: placeholderExamples });

  const { asFragment } = await waitFor(async () => render(<Library />, { wrapper: MemoryRouter }));
  expect(asFragment()).toMatchSnapshot();
});

describe('Library fetches data correctly', () => {
  test('Library fetches data on render', async () => {
    const mockedAxios = mockAxios();
    mockedAxios.mockResolvedValueOnce({ data: placeholderExamples });

    await waitFor(() => {
      render(<Library />, { wrapper: MemoryRouter });
    });
    const name = await waitFor(() => screen.getByText(placeholderExamples[0].name));
    const descriptoin = await waitFor(() =>
      screen.getByText(placeholderExamples[0].description ? placeholderExamples[0].description : 'description')
    );
    const image = await waitFor(() => screen.getByAltText(`example ${placeholderExamples[0].name} image`));
    const popup = await waitFor(() => screen.queryByText(TEXT_POPUP));

    expect(name).toBeInTheDocument();
    expect(descriptoin).toBeInTheDocument();
    expect(image).toBeInTheDocument();
    expect(popup).not.toBeInTheDocument();
    expect(mockedAxios).toHaveBeenCalledTimes(1);
  });

  test('Library fetches data on render', async () => {
    const mockedAxios = mockAxios();
    mockedAxios.mockRejectedValueOnce(new Error('Something went wrong!'));

    await waitFor(() => {
      render(<Library />, { wrapper: MemoryRouter });
    });

    const popup = await waitFor(() => screen.getByText(TEXT_POPUP));

    expect(popup).toBeInTheDocument();
    expect(mockedAxios).toHaveBeenCalledTimes(1);
  });
});
