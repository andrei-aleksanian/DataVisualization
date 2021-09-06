import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';

import axios from 'utils/axios';
import { DATA_PERSEVERANCE } from 'types/Data/DataPerseverance';

import { placeholderExamples } from 'Home/Library/Library.test';
import App from './App';
import { TEXT_LINK_CUSTOM_DATA, TEXT_LINK_LIBRARY, TEXT_H1 as TEXT_H1_HOME } from './Home';
import { TEXT_H1 as TEXT_H1_EXAMPLES } from './Home/Settings';
import { TEXT_H1 as TEXT_H1_LIBRARY } from './Home/Library';

test('App matches snapshot', async () => {
  const { asFragment } = render(<App />, { wrapper: MemoryRouter });
  expect(asFragment()).toMatchSnapshot();
});

describe('Test navigation transitions', () => {
  const init = () => {
    render(<App />, { wrapper: MemoryRouter });
  };

  test('Custom data page transition', () => {
    init();
    const linkCustom = screen.getByText(TEXT_LINK_CUSTOM_DATA);
    userEvent.click(linkCustom);

    expect(screen.getByText('Sorry, this page is not implemented yet!')).toBeInTheDocument();
  });

  test('Library page transition', async () => {
    init();
    jest.spyOn(axios, 'get').mockResolvedValueOnce({ data: placeholderExamples });
    const linkLibrary = screen.getByText(TEXT_LINK_LIBRARY);
    userEvent.click(linkLibrary);

    const libraryHeading = await waitFor(() => screen.getByText(TEXT_H1_LIBRARY));

    expect(libraryHeading).toBeInTheDocument();
  });

  test('Back to home from library', async () => {
    init();
    jest.spyOn(axios, 'get').mockResolvedValueOnce({ data: placeholderExamples });
    const linkLibrary = screen.getByText(TEXT_LINK_LIBRARY);
    userEvent.click(linkLibrary);

    const linkBack = await waitFor(() => screen.getByAltText('back'));
    userEvent.click(linkBack);

    expect(screen.getByText(TEXT_H1_HOME)).toBeInTheDocument();
  });

  test('Examples page transition', async () => {
    init();
    jest.spyOn(axios, 'get').mockResolvedValueOnce({ data: placeholderExamples });
    jest.spyOn(axios, 'post').mockResolvedValueOnce({ data: JSON.stringify(DATA_PERSEVERANCE) });

    const linkLibrary = await waitFor(() => screen.getByText(TEXT_LINK_LIBRARY));
    userEvent.click(linkLibrary);
    const linkExample = await waitFor(() => screen.getByAltText(`example ${placeholderExamples[0].name} image`));
    userEvent.click(linkExample);

    const heading = await waitFor(() => screen.getByText(TEXT_H1_EXAMPLES));
    expect(heading).toBeInTheDocument();
  });

  test('Back to library from examples', async () => {
    init();
    jest.spyOn(axios, 'get').mockResolvedValueOnce({ data: placeholderExamples });
    jest.spyOn(axios, 'get').mockResolvedValueOnce({ data: placeholderExamples });

    const linkLibrary = screen.getByText(TEXT_LINK_LIBRARY);
    userEvent.click(linkLibrary);
    const linkExample = await waitFor(() => screen.getByAltText(`example ${placeholderExamples[0].name} image`));
    userEvent.click(linkExample);

    const linkBack = await waitFor(() => screen.getByAltText('back'));
    userEvent.click(linkBack);

    const libraryHeading = await waitFor(() => screen.getByText(TEXT_H1_LIBRARY));
    expect(libraryHeading).toBeInTheDocument();
  });

  test('Back to library from errored exaxmples page', async () => {
    init();
    jest.spyOn(axios, 'get').mockResolvedValueOnce({ data: placeholderExamples });
    jest.spyOn(axios, 'post').mockRejectedValueOnce(new Error('Something went wrong'));
    jest.spyOn(axios, 'get').mockResolvedValueOnce({ data: placeholderExamples });

    const linkLibrary = screen.getByText(TEXT_LINK_LIBRARY);
    userEvent.click(linkLibrary);
    const linkExample = await waitFor(() => screen.getByAltText(`example ${placeholderExamples[0].name} image`));
    userEvent.click(linkExample);

    const linkBack = await waitFor(() => screen.getByText('OK'));
    userEvent.click(linkBack);

    const libraryHeading = await waitFor(() => screen.getByText(TEXT_H1_LIBRARY));
    expect(libraryHeading).toBeInTheDocument();
  });

  test('Back to home from custom data page', () => {
    init();
    const linkCustom = screen.getByText(TEXT_LINK_CUSTOM_DATA);
    userEvent.click(linkCustom);

    const linkBack = screen.getByAltText('back');
    userEvent.click(linkBack);

    expect(screen.getByText(TEXT_H1_HOME)).toBeInTheDocument();
  });
});
