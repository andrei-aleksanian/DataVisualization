export const RADIUS_NORMAL = 0.5;
export const RADIUS_HIGHLIGHTED = 0.7;

export const getRadius = (big: boolean) => (big ? RADIUS_HIGHLIGHTED : RADIUS_NORMAL);

let lastPointId = 0;

export const getId = (prefix = 'point-id') => {
  lastPointId += 1;
  return `${prefix}${lastPointId}`;
};
