import Slider from 'Components/Forms/Slider';

import CheckBoxes from 'Components/Forms/CheckBoxes';

export const TEXT_SLIDER_ANCHOR_DENSITY = 'Anchor density:';
export const TEXT_TOOLTIP_ANCHOR_DENSITY =
  'Determines the number of anchor points. E.g. 0.1 = nearest integer of (0.1 * number of data points)';

export const TEXT_SLIDER_EPSILON = 'Epsilon:';
export const TEXT_TOOLTIP_EPSILON = 'Controls the balance between local and global preservation performance.';

export const TEXT_CHECKBOX_ANCHOR_MODIFICATION = 'Anchor modification:';
export const TEXT_TOOLTIP_ANCHOR_MODIFICATION =
  "Whether to relocate anchor points' position according to the cohort distance relations. If 0: keep the original anchor position.";

export enum AnchorModification {
  ON,
  OFF,
}
export interface SettingsANGEL {
  anchorDensity: number;
  epsilon: number;
  anchorModification: AnchorModification;
}
export const defaultSettingsANGEL: SettingsANGEL = {
  anchorDensity: 0.1,
  epsilon: 0.1,
  anchorModification: AnchorModification.OFF,
};
export interface SettingsANGELProps {
  settingsANGEL: SettingsANGEL;
  setSettingsANGEL: React.Dispatch<React.SetStateAction<SettingsANGEL>>;
  isCustomDataPage: boolean;
}

const ANGEL = ({ settingsANGEL, setSettingsANGEL, isCustomDataPage }: SettingsANGELProps) => {
  const onChangeAnchorDensity = (value: number) => setSettingsANGEL((prev) => ({ ...prev, anchorDensity: value }));
  const onChangeEpsilon = (value: number) => setSettingsANGEL((prev) => ({ ...prev, epsilon: value }));

  const onChangeAnchorModification = (event: React.ChangeEvent, value: AnchorModification) => {
    event.preventDefault();
    setSettingsANGEL((prev) => ({ ...prev, anchorModification: value }));
  };

  return (
    <>
      <Slider
        min={isCustomDataPage ? 0.1 : 0.05}
        max={0.2}
        step={null}
        marksArr={isCustomDataPage ? [0.1, 0.2] : [0.05, 0.1, 0.2]}
        onChange={onChangeAnchorDensity}
        labelText={TEXT_SLIDER_ANCHOR_DENSITY}
        tooltipText={TEXT_TOOLTIP_ANCHOR_DENSITY}
        value={settingsANGEL.anchorDensity}
      />
      <Slider
        min={0.1}
        max={5}
        step={null}
        marksArr={[0.1, 5]}
        onChange={onChangeEpsilon}
        labelText={TEXT_SLIDER_EPSILON}
        tooltipText={TEXT_TOOLTIP_EPSILON}
        value={settingsANGEL.epsilon}
      />
      <CheckBoxes
        labelText={TEXT_CHECKBOX_ANCHOR_MODIFICATION}
        tooltipText={TEXT_TOOLTIP_ANCHOR_MODIFICATION}
        currentValue={settingsANGEL.anchorModification}
        onChange={onChangeAnchorModification}
        entries={[
          { value: AnchorModification.OFF, text: '0' },
          { value: AnchorModification.ON, text: '1' },
        ]}
      />
    </>
  );
};

export default ANGEL;
