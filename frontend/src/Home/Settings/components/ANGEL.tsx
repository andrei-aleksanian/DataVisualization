import Slider from 'Components/Forms/Slider';

import CheckBoxes from 'Components/Forms/CheckBoxes';

export const TEXT_SLIDER_ANCHOR_DENSITY = 'Anchor density:';
export const TEXT_SLIDER_EPSILON = 'Epsilon:';
export const TEXT_CHECKBOX_ANCHOR_MODIFICATION = 'Anchor modification:';

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
        text={TEXT_SLIDER_ANCHOR_DENSITY}
        value={settingsANGEL.anchorDensity}
      />
      <Slider
        min={0.1}
        max={5}
        step={null}
        marksArr={[0.1, 5]}
        onChange={onChangeEpsilon}
        text={TEXT_SLIDER_EPSILON}
        value={settingsANGEL.epsilon}
      />
      <CheckBoxes
        heading={TEXT_CHECKBOX_ANCHOR_MODIFICATION}
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
