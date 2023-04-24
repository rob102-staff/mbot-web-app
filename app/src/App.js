import React from 'react';
import './App.css';
import Sidebar from './sidebar';
import { useState } from 'react';

function App() {

  const [packageURL, setPackageURL] = useState('http://localhost/packages/default/index.html');
  
  return (
    <div className="App" id="outer-container" style={{width:"100%", height: "100vh  "}}>
      <Sidebar pageWrapId={'page-wrap'} outerContainerId={'outer-container'} setPackageURL={setPackageURL} />
      <div id="page-wrap" style={{width:"100%", height: "100%", padding: "0px"}}>
      <iframe src={packageURL} style={{ width: "100%", height: "100%", border: "0px"}}></iframe>
      </div>
    </div>
  );
}

export default App;