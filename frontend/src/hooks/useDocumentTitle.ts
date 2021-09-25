import { useEffect } from 'react';
import getDocumentTitle from 'utils/getDocumentTitle';

export default (page: string) => {
  useEffect(() => {
    document.title = getDocumentTitle(page);
  });
};
