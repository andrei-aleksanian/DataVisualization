// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';

// @ts-expect-error
window.URL.createObjectURL = () => {}; // this is here due to a weird bug in src/Home/Visualisation2D -> @react-three/drei
