import Slider from 'Components/Forms/Slider';

import CheckBoxes from 'Components/Forms/CheckBoxes';

export const TEXT_SLIDER_ALPHA = 'Alpha:';
export const TEXT_CHECKBOX_COHORT_NUMBER = 'Cohort number:';

export enum C {
  ORIGINAL,
  PERCENTAGE,
}
export interface SettingsCOVA {
  alpha: number;
  c: C;
}
export const defaultSettingsCOVA: SettingsCOVA = {
  alpha: 0,
  c: C.ORIGINAL,
};

export interface SettingsCOVAProps {
  settingsCOVA: SettingsCOVA;
  setSettingsCOVA: React.Dispatch<React.SetStateAction<SettingsCOVA>>;
}

const COVA = ({ settingsCOVA, setSettingsCOVA }: SettingsCOVAProps) => {
  const onChangeAlpha = (value: number) => setSettingsCOVA((prev) => ({ ...prev, alpha: value }));
  const onChangeC = (event: React.ChangeEvent, value: C) => {
    event.preventDefault();
    setSettingsCOVA((prev) => ({ ...prev, c: value }));
  };

  return (
    <>
      <Slider
        min={0}
        max={1}
        step={0.2}
        marksArr={[0, 0.2, 0.4, 0.6, 0.8, 1]}
        onChange={onChangeAlpha}
        text={TEXT_SLIDER_ALPHA}
        value={settingsCOVA.alpha}
      />
      <CheckBoxes
        heading={TEXT_CHECKBOX_COHORT_NUMBER}
        currentValue={settingsCOVA.c}
        onChange={onChangeC}
        entries={[
          { value: C.ORIGINAL, text: 'Original cohort number' },
          { value: C.PERCENTAGE, text: '10% of the number of points' },
        ]}
      />
    </>
  );
};

export default COVA;
