import React from 'react';
import "./location.css";

import AreaPhoto from '../../components/area';
import mockPhoto from "../../assets/image 3.png";
import Navbar from '../../components/navbar';
import { useState, useEffect } from 'react';


const Location = () => {
        const [location, setLocation] = useState(null);
        const [data, setData] = useState(null);
        const [error, setError] = useState(null);

        const fetchData = async (coords) => {
            try {
                const response = await fetch('http://localhost:8000/buildings/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(coords)
                });
                const responseData = await response.json();
                let changedData = responseData.data;
                let toChange = changedData[0]
                changedData[0] = changedData[1]
                changedData[1] = toChange
                setData(changedData)
                console.log(data)
            } catch (error) {
                setError(error);
            }
        };

        useEffect(() => {
            if (!navigator.geolocation) {
                setError('Geolocation is not supported by your browser');
                return;
            }
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const coords = {
                        lat: position.coords.latitude,
                        long: position.coords.longitude
                    };
                    setLocation(coords);
                    fetchData(coords);
                },
                (error) => {
                    setError(`Error getting location: ${error.message}`);
                }
            );
        }, []);


        if(error) {
            return <div>{error}</div>;
        }
        if (!data) {
            return <div>Loading...</div>;
        }
    // Send fetch request to back with coordinates
    // Get sorted list of locations 
    // Append photos etc..
    return (
        <>
        <div id="background">
            <Navbar/>
            {Array(Math.ceil(data.length / 3))
                .fill()
                .map((_, i) => (
                    <div className="row" key={i}>
                        {Array(3)
                            .fill()
                            .map((_, j) => (
                                <AreaPhoto
                                    key={j}
                                    link={"/leaderboard/" + data[3 * i + j].name}
                                      imgPath={data[3*i+j].image_path} active={data[3*i+j].is_accessible} name={data[3 * i + j].name}
                                ></AreaPhoto>
                            ))}
                    </div>
                ))}
        </div>
        </>
    )
}
export default Location;