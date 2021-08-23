import { render } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';

import { LinkBack, LinkHero } from './Link';

test('LinkBack matches snapshot', async () => {
  const { asFragment } = render(<LinkBack link="/" />, { wrapper: MemoryRouter });
  expect(asFragment()).toMatchSnapshot();
});

test('LinkHero matches snapshot', async () => {
  const { asFragment } = render(<LinkHero link="/" text="test link" />, { wrapper: MemoryRouter });
  expect(asFragment()).toMatchSnapshot();
});
