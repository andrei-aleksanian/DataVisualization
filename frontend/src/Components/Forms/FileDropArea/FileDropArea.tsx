import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import Error from '../Error';
import Label from '../Label';
import classes from './FileDropArea.module.scss';

export interface FileArea {
  file: File | null;
  error: string | null;
}

export interface FileDropAreaProps {
  setFile: (file: FileArea) => void;
  file: FileArea;
  acceptedType: string;
}

export const TEXT_FILEDROP_AREA = 'Choose a File:';
export const TEXT_LABEL = 'Drag and Drop or Click HERE to choose file';
export const TEST_ID = 'filearea';

const FileDropArea = ({ setFile, file: { error, file }, acceptedType }: FileDropAreaProps): React.ReactElement => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;
    setFile({ file: acceptedFiles[0], error: null });
  }, []);
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    maxFiles: 1,
    onDrop,
    accept: acceptedType,
  });

  return (
    <>
      <Label text={TEXT_FILEDROP_AREA} customCalss={classes.label} />
      <div className={classes.Wrapper}>
        <div
          style={{
            borderColor: isDragActive ? 'var(--color-action)' : '#bbb', // stylelint-disable-line
          }}
          {...getRootProps({ className: classes.Container })}
        >
          <input {...getInputProps()} data-testid={TEST_ID} />
          <label>{TEXT_LABEL}</label>
        </div>
      </div>
      {file && <p className={classes.fileName}>Submitted file: {file.name}</p>}
      {error && <Error text={error} />}
    </>
  );
};

export default FileDropArea;
