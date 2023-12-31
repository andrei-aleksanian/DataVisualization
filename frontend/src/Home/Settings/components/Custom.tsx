import hostLink from 'utils/hostLink';

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
  setSettingsCustom: React.Dispatch<React.SetStateAction<SettingsCustom>>;
  settingsCustom: SettingsCustom;
  acceptedType: string;
}
export const TEXT_CHECKBOX_DIMENSION = 'Dimension:';
export const TEXT_TOOLTIP_CHECKBOX_DIMENSION = 'Choose the target dimension of your visualization.';
export const TEXT_FILEDROP_AREA = 'Choose a File:';
export const TEXT_TOOLTIP_FILEDROP_AREA =
  "Currently we only support .mat files. The format is: 'g': Data matrix, 'label': Cohort label column.";
export const HTML_LINK_FILEDROP_AREA = (
  <a
    href={`${hostLink}/api/dynamic/exampleMat/bicycle_sample.mat`}
    className={classes.link}
    target="_blank"
    rel="noreferrer"
  >
    See Example file here
  </a>
);

const Custom = ({ setSettingsCustom, settingsCustom: { dimension, file }, acceptedType }: CustomProps) => {
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
        labelText={TEXT_CHECKBOX_DIMENSION}
        tooltipText={TEXT_TOOLTIP_CHECKBOX_DIMENSION}
        currentValue={dimension}
        onChange={onChangeDimension}
        entries={[
          { value: Dimension.D2, text: '2' },
          { value: Dimension.D3, text: '3' },
        ]}
      />
      <FileDropArea
        setFile={setFile}
        file={file}
        acceptedType={acceptedType}
        tooltipText={TEXT_TOOLTIP_FILEDROP_AREA}
        labelText={TEXT_FILEDROP_AREA}
        toolitipLink={HTML_LINK_FILEDROP_AREA}
      />
    </div>
  );
};

export default Custom;

export const TEXT_BUTTON = 'Submit';
export interface SubmitProps {
  error: string | null;
  onSubmit: Function;
}
export const Submit = ({ error, onSubmit }: SubmitProps) => (
  <>
    <Button text={TEXT_BUTTON} onClick={() => onSubmit()} active={false} />
    {error && <Error text={error} />}
  </>
);
