import FileDropArea, { FileDropAreaProps, Validation } from 'Components/Forms/FileDropArea';
import Button from 'Components/Forms/Button';

export interface CustomProps {
  onSubmit: Function;
  setFile: FileDropAreaProps['setFile'];
  validation: Validation;
}

const Custom = ({ onSubmit, setFile, validation }: CustomProps) => {
  return (
    <div>
      <FileDropArea setFile={setFile} validation={validation} />
      <Button text="Submit" onClick={() => onSubmit()} active={false} />
    </div>
  );
};

export default Custom;
