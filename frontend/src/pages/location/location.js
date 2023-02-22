import React from 'react';
import "./location.css";

import AreaPhoto from '../../components/area';
import mockPhoto from "../../assets/image 3.png";
import Navbar from '../../components/navbar';
import { useState, useEffect } from 'react';
const Location = () => {


    const [latitude, setLatitude] = useState(null);
    const [longitude, setLongitude] = useState(null);
    const [error, setError] = useState(null);
  
    useEffect(() => {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLatitude(position.coords.latitude);
          setLongitude(position.coords.longitude);
        },
        (error) => {
          setError(error.message);
        }
      );
    }, []);

    // Send fetch request to back with coordinates
    // Get sorted list of locations 
    // Append photos etc..
    

    return (
        <>
        <div id = 'background'>
            <Navbar/>
            <div>
            {latitude && longitude ? (
        <p>
          Your latitude is {latitude.toFixed(2)}, and your longitude is{' '}
          {longitude.toFixed(2)}.
        </p>
      ) : error ? (
        <p>{error}</p>      
      ) : (
        <p>Getting your location...</p>
      )}
            </div>
            <div className='row'>
                <AreaPhoto link={"/leaderboard/forum"} imgPath={mockPhoto}></AreaPhoto>
                <AreaPhoto link={"/leaderboard/forum"} imgPath={mockPhoto}></AreaPhoto>
                <AreaPhoto link={"/leaderboard/forum"} imgPath={mockPhoto}></AreaPhoto>
                </div>
            <div className='row'>
            <AreaPhoto linsk={"/leaderboard/forum"} imgPath={mockPhoto}></AreaPhoto>
                <AreaPhoto link={"/leaderboard/forum"} imgPath={mockPhoto}></AreaPhoto>
                <AreaPhoto link={"/leaderboard/forum"} imgPath={mockPhoto}></AreaPhoto>
                </div>
        </div>
        </>
    )
}
export default Location;