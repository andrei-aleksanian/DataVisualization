export const RADIUS_NORMAL = 0.5;
export const RADIUS_HIGHLIGHTED = 0.6;

export const getRadius = (big: boolean) => {
  return big ? RADIUS_HIGHLIGHTED : RADIUS_NORMAL;
};
