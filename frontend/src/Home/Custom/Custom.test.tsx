import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import axios from 'utils/axios';

import { DATA_PERSEVERANCE } from 'types/Data/DataPerseverance';

import { TEST_ID } from 'Components/Forms/FileDropArea';
import { TEXT_BUTTON } from 'Home/Settings';
import Custom, { TEXT_FILE_NULL } from '.';

const mockAxios = () => {
  return jest.spyOn(axios, 'post');
};

test('Examples matches snapshot', async () => {
  const { asFragment } = render(<Custom />, { wrapper: MemoryRouter });
  expect(asFragment()).toMatchSnapshot();
});

describe('Examples fetches data correctly', () => {
  test('Success fetch data on click', async () => {
    const mockedAxios = mockAxios();
    mockedAxios.mockResolvedValueOnce({ data: DATA_PERSEVERANCE });
    mockedAxios.mockResolvedValueOnce({ data: { ...DATA_PERSEVERANCE, iteration: DATA_PERSEVERANCE.maxIteration } });
    render(<Custom />, { wrapper: MemoryRouter });

    const file = new File(['hello'], 'hello.mat', { type: '.mat' });
    const fileArea = screen.getByTestId(TEST_ID) as HTMLInputElement;
    await waitFor(() => userEvent.upload(fileArea, file));

    const submit = screen.getByText(TEXT_BUTTON);
    await waitFor(async () => userEvent.click(submit));

    // after 2 iterations of side effects, the canvas should be in the document
    const canvas = await screen.findByTestId('canvas');
    const error = screen.queryByText('custom-error');
    expect(canvas).toBeInTheDocument();
    expect(error).not.toBeInTheDocument();
    // the algorithm must stop when iterations == maxIterations
    expect(mockedAxios).toHaveBeenCalledTimes(2);
  });

  test('Fail no file', async () => {
    const mockedAxios = mockAxios();
    render(<Custom />, { wrapper: MemoryRouter });

    const submit = screen.getByText(TEXT_BUTTON);
    await waitFor(() => userEvent.click(submit));

    // when providing no .mat file, the algorithm must not run
    // and the error message should appear
    // canvas has no data to be renderred on
    const error = await screen.findByText(TEXT_FILE_NULL);
    const canvas = screen.queryByTestId('canvas');

    expect(error).toBeInTheDocument();
    expect(canvas).not.toBeInTheDocument();
    expect(mockedAxios).not.toHaveBeenCalled();
  });

  test('Fail wrong file', async () => {
    const mockedAxios = mockAxios();
    render(<Custom />, { wrapper: MemoryRouter });

    const file = new File(['hello'], 'hello.jpg', { type: '.jpg' });
    const fileArea = screen.getByTestId(TEST_ID) as HTMLInputElement;
    await waitFor(() => userEvent.upload(fileArea, file));

    const submit = screen.getByText(TEXT_BUTTON);
    await waitFor(() => userEvent.click(submit));

    // when providing a non .mat file, the algorithm must not run
    // and the error message should appear
    // canvas has no data to be renderred on
    const error = await screen.findByText(TEXT_FILE_NULL);
    const canvas = screen.queryByTestId('canvas');

    expect(error).toBeInTheDocument();
    expect(canvas).not.toBeInTheDocument();
    expect(mockedAxios).not.toHaveBeenCalled();
  });

  test('Fail something went wrong on the server', async () => {
    const mockedAxios = mockAxios();
    const ERROR_MESSAGE = 'Oops';
    mockedAxios.mockRejectedValueOnce(new Error(ERROR_MESSAGE));
    mockedAxios.mockResolvedValueOnce({ data: DATA_PERSEVERANCE });
    mockedAxios.mockResolvedValueOnce({ data: { ...DATA_PERSEVERANCE, iteration: DATA_PERSEVERANCE.maxIteration } });
    render(<Custom />, { wrapper: MemoryRouter });

    const file = new File(['hello'], 'hello.mat', { type: '.mat' });
    const fileArea = screen.getByTestId(TEST_ID) as HTMLInputElement;
    await waitFor(() => userEvent.upload(fileArea, file));

    const submit = screen.getByText(TEXT_BUTTON);
    await waitFor(() => userEvent.click(submit));

    // when the server throws an error
    // the algorithm should stop and
    // show an error message
    const error = await screen.findByText(ERROR_MESSAGE);
    const canvas = screen.queryByTestId('canvas');

    expect(error).toBeInTheDocument();
    expect(canvas).not.toBeInTheDocument();
    expect(mockedAxios).toHaveBeenCalledTimes(1);
  });
});
