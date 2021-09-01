import Slider from 'Components/Forms/Slider';

import CheckBoxes from 'Components/Forms/CheckBoxes';

export const TEXT_SLIDER_ANCHOR_DENSITY = 'Anchor density:';
export const TEXT_SLIDER_EPSILON = 'Epsilon:';
export const TEXT_CHECKBOX_ANCHOR_MODIFICATION = 'Anchor modification:';

export enum FlagMove {
  ON,
  OFF,
}
export interface SettingsANGEL {
  sparsity: number;
  epsilon: number;
  flagMove: FlagMove;
}
export const defaultSettingsANGEL: SettingsANGEL = {
  sparsity: 0.05,
  epsilon: 0.5,
  flagMove: FlagMove.OFF,
};
export interface SettingsANGELProps {
  settingsANGEL: SettingsANGEL;
  setSettingsANGEL: React.Dispatch<React.SetStateAction<SettingsANGEL>>;
}

const ANGEL = ({ settingsANGEL, setSettingsANGEL }: SettingsANGELProps) => {
  const onChangeSparsity = (value: number) => setSettingsANGEL((prev) => ({ ...prev, sparsity: value }));
  const onChangeEpsilon = (value: number) => setSettingsANGEL((prev) => ({ ...prev, epsilon: value }));

  const onChangeFlagMove = (event: React.ChangeEvent, value: FlagMove) => {
    event.preventDefault();
    setSettingsANGEL((prev) => ({ ...prev, flagMove: value }));
  };

  return (
    <>
      <Slider
        min={0.05}
        max={0.2}
        step={null}
        marksArr={[0.05, 0.1, 0.2]}
        onChange={onChangeSparsity}
        text={TEXT_SLIDER_ANCHOR_DENSITY}
        value={settingsANGEL.sparsity}
      />
      <Slider
        min={0.5}
        max={5}
        step={null}
        marksArr={[0.5, 5]}
        onChange={onChangeEpsilon}
        text={TEXT_SLIDER_EPSILON}
        value={settingsANGEL.epsilon}
      />
      <CheckBoxes
        heading={TEXT_CHECKBOX_ANCHOR_MODIFICATION}
        currentValue={settingsANGEL.flagMove}
        onChange={onChangeFlagMove}
        entries={[
          { value: FlagMove.OFF, text: '0' },
          { value: FlagMove.ON, text: '1' },
        ]}
      />
    </>
  );
};

export default ANGEL;
