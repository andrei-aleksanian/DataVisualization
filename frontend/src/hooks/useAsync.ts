/**
 * wrapper for useEffect which stops the hook if the component is unmounted.
 * currently unused
 */
import { useEffect } from 'react';

export default (asyncFn: Function, onSuccess: Function) => {
  useEffect(() => {
    let isActive = true;
    const asyncHelper = async () => {
      const data = await asyncFn();
      if (isActive) onSuccess(data);
    };
    asyncHelper();
    return () => {
      isActive = false;
    };
  }, [asyncFn, onSuccess]);
};
