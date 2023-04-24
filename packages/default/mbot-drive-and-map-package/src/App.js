import './App.css';
import DriveController from './DriveController';

function App() {
  return (
    <div className="App">
      <div style={{width: "100%", height: "100%", display: "flex", flexDirection: "column"}}>
      <h1>Sample Drive Controller and Map package</h1>
      <DriveController />
      </div>
    </div>
  );
}

export default App;
