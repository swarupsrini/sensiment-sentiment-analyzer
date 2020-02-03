import React, { useEffect, useState } from "react";
import "./App.css";
import Upload from "./Components/Upload";
import Chart from "./Components/Chart";
import Loader from "./Components/Loader";
import Header from "./Components/Header";
import AudioAnalyser from "react-audio-analyser";

class Record extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      status: null
    };
  }

  controlAudio(status) {
    this.setState({
      status
    });
  }

  render() {
    const { status, audioSrc } = this.state;
    const audioProps = {
      audioType: "audio/wav", // Temporarily only supported audio/wav, default audio/webm
      status, // Triggering component updates by changing status
      audioSrc,
      startCallback: e => {
        console.log("succ start", e);
      },
      pauseCallback: e => {
        console.log("succ pause", e);
      },
      stopCallback: e => {
        this.setState({
          audioSrc: window.URL.createObjectURL(e)
        });
        console.log("succ stop", e);
      }
    };
    return (
      <AudioAnalyser {...audioProps}>
        <div className="btn-box">
          {status !== "recording" && (
            <button onClick={() => this.controlAudio("recording")}>
              start
            </button>
          )}
          {status === "recording" && (
            <button onClick={() => this.controlAudio("paused")}>pause</button>
          )}
          <button onClick={() => this.controlAudio("inactive")}>stop</button>
        </div>
      </AudioAnalyser>
    );
  }
}

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
      <Record />
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
