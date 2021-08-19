export const RADIUS_NORMAL = 0.5;
export const RADIUS_HIGHLIGHTED = 0.7;

export const getRadius = (big: boolean) => (big ? RADIUS_HIGHLIGHTED : RADIUS_NORMAL);
