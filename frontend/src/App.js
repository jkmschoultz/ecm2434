import logo from './logo.svg';
import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [currentTime, setCurrentTime] = useState(0);
  const [currentDate, setCurrentDate] = useState(0);
  useEffect(() => {
  fetch(' http://127.0.0.1:8000/').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
      setCurrentDate(data.date);
      console.log("dfdf");
    });
  }, []);
  return (
    <div className="App">
      <header className="App-header">
      <p>The date is {currentDate} and the (probably wrong) time is {currentTime}. This is the change for checking docker updattes.</p> <br/>

      </header>
    </div>
  );
}

export default App;
