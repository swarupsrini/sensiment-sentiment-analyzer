import React, { useEffect, useState } from "react";
import "./App.css";
import Upload from "./Components/Upload";
import Chart from "./Components/Chart";
import Loader from "./Components/Loader";
import Header from "./Components/Header";

const App = () => {
  const [data, setData] = useState([]);
  const [receivedFiles, setReceivedFiles] = useState([]);
  const handleSentiment = sentiment => {
    console.log(sentiment);
    setData([...data, sentiment]);
  };
  useEffect(() => {}, []);
  return (
    <div className="App">
      <Header />
      <Upload
        onReceivedSentiment={handleSentiment}
        onReceivedFiles={newFile =>
          setReceivedFiles([...receivedFiles, newFile])
        }
      />
      <div style={{ width: "80vw", height: "400px" }}>
        {data.length ? (
          <div>
            {data.map(entry => (
              <>
                <div className="card">
                  <h3>{entry.name}</h3>
                  <p>
                    <strong>keywords:</strong> {entry.keywords}
                  </p>
                  <p>
                    <strong>text detected:</strong> {entry.text}
                  </p>
                </div>
                <div
                  className="card"
                  style={{ width: "80vw", height: "400px" }}
                >
                  <Chart data={entry.items} />
                </div>
              </>
            ))}
          </div>
        ) : null}
      </div>
    </div>
  );
};

export default App;
