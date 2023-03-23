import React from 'react';
import "./location.css";

import AreaPhoto from '../../components/area';
import mockPhoto from "../../assets/image 3.png";
import Navbar from '../../components/navbar';
import { useState, useEffect } from 'react';
import axiosInstance from "../../axios";

//Main page with location choice
const Location = () => {
        const [location, setLocation] = useState(null);
        const [data, setData] = useState(null);
        const [error, setError] = useState(null);

        //function to set array of buildings and swapping first and last element
        const fetchData = async (coords) => {
            try {
                const response = await axiosInstance.post('buildings/', coords);
                const responseData = response.data;
                let changedData = responseData.data;
                let toChange = changedData[0];
                changedData[0] = changedData[1];
                changedData[1] = toChange;
                setData(changedData);
            } catch (error) {
                setError(error);
            }
        };

        //on page render ask for user's geolocation and send it to server using fetchData
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
            return <div>{error}. Please run away, something terrible happeneds</div>;
        }
        if (!data) {
            return <div>
                Loading... Saving turtles meanwhile...🐢🐢🐢
            </div>
        }
    //dynamically fill locations to have all locations displayed
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
                                      imgPath={"http://"+data[3*i+j].image_path} active={data[3*i+j].is_accessible} name={data[3 * i + j].name}
                                    floors = {data[3*i+j].floors}
                                ></AreaPhoto>
                            ))}
                    </div>
                ))}
        </div>
        </>
    )
}
export default Location;