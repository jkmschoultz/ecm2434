import logo from './logo.svg';
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Location from './pages/location/location.js';
import './App.css';
import Leaderboard from "./pages/leaderboard/leaderboard";
import Profile from "./pages/profile/profile";

function App() {
  // const [currentTime, setCurrentTime] = useState(0);
  // const [currentDate, setCurrentDate] = useState(0);
  // useEffect(() => {
  // fetch(' http://127.0.0.1:8000/').then(res => res.json()).then(data => {
  //     setCurrentTime(data.time);
  //     setCurrentDate(data.date);
  //     console.log("dfdf");
  //   });
  // }, []);
  return (
    <>
        <Router>
          <Routes>
            <Route path='/location' element = {<Location></Location>}></Route>
              <Route path="/leaderboard/:code" element ={<Leaderboard></Leaderboard>} />
              <Route path = "/profile" element = {<Profile> </Profile>}> </Route>
            <Route path = '/cake' element = {<div>cake</div>}></Route>
          </Routes>
        </Router>
    </>
  );
}

export default App;
