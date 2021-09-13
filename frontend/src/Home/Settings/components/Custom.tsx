import FileDropArea, { Validation } from 'Components/Forms/FileDropArea';
import Button from 'Components/Forms/Button';
import CheckBoxes from 'Components/Forms/CheckBoxes';

export enum Dimension {
  D2,
  D3,
}
export interface SettingsCustom {
  dimension: Dimension;
  validation: Validation;
  file: File | null;
}
export interface CustomProps {
  onSubmit: Function;
  setSettingsCustom: React.Dispatch<React.SetStateAction<SettingsCustom>>;
  settingsCustom: SettingsCustom;
}

export const TEXT_CHECKBOX_DIMENSION = 'Dimension:';

const Custom = ({ onSubmit, setSettingsCustom, settingsCustom: { validation, dimension } }: CustomProps) => {
  const onChangeDimension = (event: React.ChangeEvent, value: Dimension) => {
    event.preventDefault();
    setSettingsCustom((prev) => ({ ...prev, dimension: value }));
  };
  const setFile = (value: File) => {
    setSettingsCustom((prev) => ({ ...prev, file: value }));
  };
  const setValidation = (value: boolean) => {
    setSettingsCustom((prev) => ({ ...prev, validation: { validation: value } }));
  };

  return (
    <div>
      <CheckBoxes
        heading={TEXT_CHECKBOX_DIMENSION}
        currentValue={dimension}
        onChange={onChangeDimension}
        entries={[
          { value: Dimension.D2, text: '2' },
          { value: Dimension.D3, text: '3' },
        ]}
      />
      <FileDropArea setFile={setFile} setValidation={setValidation} validation={validation} />
      <Button text="Submit" onClick={() => onSubmit()} active={false} />
    </div>
  );
};

export default Custom;