import './App.css';
import roslib from 'roslib';
import { useState, useEffect } from 'react';

function App() {
  const [topics, setTopics] = useState([]);
  const [topicTypes, setTopicTypes] = useState([]);
  useEffect(() => {
    const ros = new roslib.Ros({
      url: 'ws://localhost:9090'
    });

    ros.on('connection', function () {
      console.log('Connected to websocket server.');
    });

    ros.on('error', function (error) {
      console.log('Error connecting to websocket server: ', error);
    });

    ros.on('close', function () {
      console.log('Connection to websocket server closed.');
    });

    // get all topics
    ros.getTopics(function (topics) {
      console.log(topics);
      setTopics(topics.topics); // set the topics state
      setTopicTypes(topics.types); // set the topic types state
    });
  }, []);

  return (
    <div className="App" style={{ display: "flex", alignItems: "center", flexDirection: "column" }}>
      <h1>Sample ROS2 diagnostics package for the mbot app</h1>
      <h2>Topics</h2>
      {topics.map((topic, index) => {
        return (<div key={index}>
          <h3 style={{marginBottom: "0px", paddingBottom: "0px"}} >{topic}</h3>
          <p style={{marginTop:"1px"}}>{topicTypes[index]}</p>
        </div>)
      }
      )}
    </div>
  );
}

export default App;
