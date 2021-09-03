import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';

import axios from 'utils/axios';
import { DATA_PERSEVERANCE } from 'types/Data/DataPerseverance';

import App from './App';
import { TEXT_LINK_CUSTOM_DATA, TEXT_LINK_EXAMPLES, TEXT_H1 as TEXT_H1_HOME } from './Home';
import { TEXT_H1 } from './Home/Settings';

test('App matches snapshot', async () => {
  const { asFragment } = render(<App />, { wrapper: MemoryRouter });
  expect(asFragment()).toMatchSnapshot();
});

describe('Test navigation transitions', () => {
  const init = () => {
    render(<App />, { wrapper: MemoryRouter });
  };

  test('Examples page transition', () => {
    init();
    const linkExamples = screen.getByText(TEXT_LINK_EXAMPLES);
    userEvent.click(linkExamples);

    expect(screen.getByText(TEXT_H1)).toBeInTheDocument();
  });

  test('Custom data page transition', () => {
    init();
    const linkCustom = screen.getByText(TEXT_LINK_CUSTOM_DATA);
    userEvent.click(linkCustom);

    expect(screen.getByText('Sorry, this page is not implemented yet!')).toBeInTheDocument();
  });

  test('Back to home from examples', () => {
    init();
    const linkExamples = screen.getByText(TEXT_LINK_EXAMPLES);
    userEvent.click(linkExamples);

    const linkBack = screen.getByAltText('back');
    userEvent.click(linkBack);

    expect(screen.getByText(TEXT_H1_HOME)).toBeInTheDocument();
  });

  test('Back to home from errored exaxmples page', async () => {
    init();
    // mocking the post(actually get) request in useEffect
    jest.spyOn(axios, 'post').mockRejectedValueOnce({ data: JSON.stringify(DATA_PERSEVERANCE) });

    const linkExamples = screen.getByText(TEXT_LINK_EXAMPLES);
    userEvent.click(linkExamples);

    const linkBack = await waitFor(() => screen.getByText('OK'));
    userEvent.click(linkBack);

    expect(screen.getByText(TEXT_H1_HOME)).toBeInTheDocument();
  });

  test('Back to home from custom data page', () => {
    init();
    const linkExamples = screen.getByText(TEXT_LINK_CUSTOM_DATA);
    userEvent.click(linkExamples);

    const linkBack = screen.getByAltText('back');
    userEvent.click(linkBack);

    expect(screen.getByText(TEXT_H1_HOME)).toBeInTheDocument();
  });
});
