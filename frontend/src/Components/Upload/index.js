import React, { useCallback, useState, useMemo } from "react";
import { useDropzone } from "react-dropzone";
import Loader from "../Loader";

const SERVER_URL = window.location.href;
console.log(SERVER_URL);

const baseStyle = {
  flex: 1,
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  padding: "20px",
  borderWidth: 2,
  borderRadius: 2,
  borderColor: "#eeeeee",
  borderStyle: "dashed",
  backgroundColor: "#fafafa",
  color: "#bdbdbd",
  outline: "none",
  transition: "border .24s ease-in-out"
};

const activeStyle = {
  borderColor: "#2196f3"
};

const acceptStyle = {
  borderColor: "#00e676"
};

const rejectStyle = {
  borderColor: "#ff1744"
};

const Upload = ({ onReceivedFiles, onReceivedSentiment }) => {
  const [currFile, setCurrFile] = useState();
  const [isLoading, setIsLoading] = useState(false);

  const sendToServer = async file => {
    setIsLoading(true);
    const resp = await fetch(
      `${SERVER_URL}/getSentimentDataStream?name=${file.path}`,
      {
        method: "POST",
        body: file
      }
    );
    const json = await resp.json();
    onReceivedSentiment(json);
    console.log(json);
    setIsLoading(false);
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
        setCurrFile(fileInfo);
        onReceivedFiles(file.path);
      };
      reader.readAsArrayBuffer(file);
    });
  }, []);

  const {
    getRootProps,
    getInputProps,
    isDragActive,
    isDragReject,
    isDragAccept
  } = useDropzone({ onDrop });

  const style = useMemo(
    () => ({
      ...baseStyle,
      ...(isDragActive ? activeStyle : {}),
      ...(isDragAccept ? acceptStyle : {}),
      ...(isDragReject ? rejectStyle : {})
    }),
    [isDragActive, isDragReject]
  );
  return (
    <div {...getRootProps()} style={style}>
      <input {...getInputProps()} />
      {isDragActive ? (
        <p>Drop the audio files here ...</p>
      ) : (
        <p>Drag 'n' drop some files here, or click to select files</p>
      )}
      {currFile}
      {isLoading && <Loader />}
    </div>
  );
};

export default Upload;
