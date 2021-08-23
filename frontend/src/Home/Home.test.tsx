import { render } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';

import Home from './Home';

test('Settings matches snapshot', async () => {
  const { asFragment } = render(<Home />, { wrapper: MemoryRouter });
  expect(asFragment()).toMatchSnapshot();
});
