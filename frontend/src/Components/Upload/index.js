import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";

console.log(`${window.location.href}:${process.env.PORT}`);

const Upload = () => {
  const [receivedFiles, setReceivedFiles] = useState([]);

  const sendToServer = file => {
    fetch(`${window.location.href}:${process.env.PORT}/getSentimentData`, {
      method: "POST",
      body: file
    })
      .then(resp => resp.json())
      .catch(error => console.log(error));
  };

  const onDrop = useCallback(acceptedFiles => {
    acceptedFiles.forEach(file => {
      const reader = new FileReader();

      reader.onabort = () => console.log("file reading was aborted");
      reader.onerror = () => console.log("file reading has failed");
      reader.onload = () => {
        // Do whatever you want with the file contents
        const binaryStr = reader.result;
        console.log(binaryStr);
        sendToServer(file);
        const fileInfo = (
          <li key={file.path}>
            {file.path} - {file.size} bytes
          </li>
        );
        setReceivedFiles([...receivedFiles, fileInfo]);
      };
      reader.readAsArrayBuffer(file);
    });
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <div {...getRootProps()}>
      <input {...getInputProps()} />
      {isDragActive ? (
        <p>Drop the audio files here ...</p>
      ) : (
        <p>Drag 'n' drop some files here, or click to select files</p>
      )}
      {receivedFiles}
    </div>
  );
};

export default Upload;
