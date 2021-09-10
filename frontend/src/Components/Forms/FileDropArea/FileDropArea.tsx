import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import classes from './FileDropArea.module.scss';

const getcolor = ({
  isDragActive,
  isDragAccept,
  isDragReject,
}: {
  isDragActive: boolean;
  isDragAccept: boolean;
  isDragReject: boolean;
}) => {
  if (isDragAccept) {
    return '#00e676';
  }
  if (isDragReject) {
    return '#ff1744';
  }
  if (isDragActive) {
    return '#2196f3';
  }
  return '#eeeeee';
};

export interface Validation {
  setValidation: React.Dispatch<React.SetStateAction<boolean>>;
  validation: boolean;
  validationMessage?: string;
}

export interface FileDropAreaProps {
  setFile: React.Dispatch<React.SetStateAction<File | null>>;
  validation: Validation;
}

export const FILE_NOT_FOUND = 'Please, provide a .mat file';

const FileDropArea = ({
  setFile,
  validation: { setValidation, validation, validationMessage },
}: FileDropAreaProps): React.ReactElement => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFile(acceptedFiles[0]);
    setValidation(acceptedFiles[0] === null);
  }, []);
  const { getRootProps, getInputProps, isDragActive, isDragAccept, isDragReject } = useDropzone({
    maxFiles: 1,
    onDrop,
  });

  return (
    <>
      <div
        style={{
          borderColor: getcolor({ isDragActive, isDragAccept, isDragReject }), // stylelint-disable-line
        }}
        {...getRootProps({ className: classes.Container })}
      >
        <input {...getInputProps()} />
        <p>Drag and Drop or Click HERE to choose file</p>
      </div>
      {validation && <span className={classes.error}>{validationMessage || FILE_NOT_FOUND}</span>}
    </>
  );
};

export default FileDropArea;
