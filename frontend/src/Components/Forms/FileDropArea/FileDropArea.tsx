import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import Error from '../Error';
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
    return 'var(--color-action)';
  }
  if (isDragReject) {
    return 'var(--color-error)';
  }
  if (isDragActive) {
    return '#2196f3';
  }
  return '#bbb';
};

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

const FileDropArea = ({ setFile, file: { error, file }, acceptedType }: FileDropAreaProps): React.ReactElement => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;
    setFile({ file: acceptedFiles[0], error: null });
  }, []);
  const { getRootProps, getInputProps, isDragActive, isDragAccept, isDragReject } = useDropzone({
    maxFiles: 1,
    onDrop,
    accept: acceptedType,
  });

  return (
    <>
      <p className={classes.p}>{TEXT_FILEDROP_AREA}</p>
      <div className={classes.Wrapper}>
        <div
          style={{
            borderColor: getcolor({ isDragActive, isDragAccept, isDragReject }), // stylelint-disable-line
          }}
          {...getRootProps({ className: classes.Container })}
        >
          <input {...getInputProps()} />
          <p>Drag and Drop or Click HERE to choose file</p>
        </div>
      </div>
      {file && <p className={classes.fileName}>Submitted file: {file.name}</p>}
      {error && <Error text={error} />}
    </>
  );
};

export default FileDropArea;
