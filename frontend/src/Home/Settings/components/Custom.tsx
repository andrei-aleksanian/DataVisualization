import FileDropArea, { FileArea } from 'Components/Forms/FileDropArea';
import Button from 'Components/Forms/Button';
import CheckBoxes from 'Components/Forms/CheckBoxes';
import Error from 'Components/Forms/Error';

import classes from '../Settings.module.scss';

export enum Dimension {
  D2,
  D3,
}
export interface SettingsCustom {
  dimension: Dimension;
  file: FileArea;
}
export const defaultSettingsCustom: SettingsCustom = {
  file: { file: null, error: null },
  dimension: Dimension.D2,
};
export interface CustomProps {
  onSubmit: Function;
  setSettingsCustom: React.Dispatch<React.SetStateAction<SettingsCustom>>;
  settingsCustom: SettingsCustom;
  error: string | null;
  acceptedType: string;
}

export const TEXT_CHECKBOX_DIMENSION = 'Dimension:';
export const TEXT_BUTTON = 'Submit';

const Custom = ({
  onSubmit,
  setSettingsCustom,
  settingsCustom: { dimension, file },
  error,
  acceptedType,
}: CustomProps) => {
  const onChangeDimension = (event: React.ChangeEvent, value: Dimension) => {
    event.preventDefault();
    setSettingsCustom((prev) => ({ ...prev, dimension: value }));
  };
  const setFile = (fileNew: FileArea) => {
    setSettingsCustom((prev) => ({ ...prev, file: fileNew }));
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
      <FileDropArea setFile={setFile} file={file} acceptedType={acceptedType} />
      <Button text={TEXT_BUTTON} onClick={() => onSubmit()} active={false} customClass={classes.submit} />
      {error && <Error text={error} />}
    </div>
  );
};

export default Custom;
