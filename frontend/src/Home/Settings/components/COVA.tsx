import Slider from 'Components/Forms/Slider';

import CheckBoxes from 'Components/Forms/CheckBoxes';

export const TEXT_SLIDER_ALPHA = 'Alpha:';
export const TEXT_TOOLTIP_ALPHA =
  'Controls the balance between local and global preservation performance. From 0 to 1 is from local to global.';
export const TEXT_CHECKBOX_COHORT_NUMBER = 'Cohort number:';
export const TEXT_TOOLTIP_COHORT_NUMBER =
  'The original cohort number keeps the same cohort as the original dataset. The 10% number of points re-cluster the original dataset into some smaller cohorts where the cohort number equals to 10% number of points.';

export enum CohortNumber {
  ORIGINAL,
  PERCENTAGE,
}
export interface SettingsCOVA {
  alpha: number;
  cohortNumber: CohortNumber;
}
export const defaultSettingsCOVA: SettingsCOVA = {
  alpha: 0.4,
  cohortNumber: CohortNumber.PERCENTAGE,
};

export interface SettingsCOVAProps {
  settingsCOVA: SettingsCOVA;
  setSettingsCOVA: React.Dispatch<React.SetStateAction<SettingsCOVA>>;
}

const COVA = ({ settingsCOVA, setSettingsCOVA }: SettingsCOVAProps) => {
  const onChangeAlpha = (value: number) => setSettingsCOVA((prev) => ({ ...prev, alpha: value }));
  const onChangeCohortNumber = (event: React.ChangeEvent, value: CohortNumber) => {
    event.preventDefault();
    setSettingsCOVA((prev) => ({ ...prev, cohortNumber: value }));
  };

  return (
    <>
      <Slider
        min={0}
        max={1}
        step={0.2}
        marksArr={[0, 0.2, 0.4, 0.6, 0.8, 1]}
        onChange={onChangeAlpha}
        labelText={TEXT_SLIDER_ALPHA}
        tooltipText={TEXT_TOOLTIP_ALPHA}
        value={settingsCOVA.alpha}
      />
      <CheckBoxes
        labelText={TEXT_CHECKBOX_COHORT_NUMBER}
        tooltipText={TEXT_TOOLTIP_COHORT_NUMBER}
        currentValue={settingsCOVA.cohortNumber}
        onChange={onChangeCohortNumber}
        entries={[
          { value: CohortNumber.ORIGINAL, text: 'Original cohort number' },
          { value: CohortNumber.PERCENTAGE, text: '10% of the number of points' },
        ]}
      />
    </>
  );
};

export default COVA;
