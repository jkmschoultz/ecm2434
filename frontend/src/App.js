import logo from './logo.svg';
import React, { useState, useEffect } from 'react';
import {BrowserRouter as Router, Routes, Route} from "react-router-dom";
import Location from './pages/location/location.js';
import './App.css';
import Leaderboard from "./pages/leaderboard/leaderboard";
import Profile from "./pages/profile/profile";
import Quiz from "./pages/quiz/quiz";
import Main from "./pages/main/main";
import Register from "./pages/register/register";
import protectedRoute from "./components/protectedRoute";
import ProtectedRoute from "./components/protectedRoute";
import Shop from "./pages/shop/shop";
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
            <Route path = "/" element = {<Main></Main>}></Route>
            <Route path='/location' element = {<Location></Location>}></Route>
            <Route path="/leaderboard/:code" element ={<Leaderboard></Leaderboard>} />
            <Route path = "/profile" element = {<ProtectedRoute/>}>
              <Route index element = {<Profile></Profile>}></Route>
            </Route>
            <Route path = '/quiz' element = {<ProtectedRoute></ProtectedRoute>}>
              <Route index element = {<Quiz/>}></Route>
            </Route>
            <Route path = '/shop' element = {<ProtectedRoute></ProtectedRoute>}>
              <Route index element = {<Shop/>}></Route>
            </Route>
            <Route path = '/cake' element = {<div>cake</div>}></Route>
            <Route path = '/register' element = {<Register></Register>}></Route>
          </Routes>
        </Router>
    </>
  );
}

export default App;
