import React from 'react';

import classes from "./main.css";

import greenNavbar from "../../components/greenNavbar";
import GreenNavbar from "../../components/greenNavbar";
import LoginPopup from "../../components/loginPopup";
const Main = () => {


    return (
        <>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"/>
        <GreenNavbar></GreenNavbar>
        <div className="container-fluid p-0">
            <div className="site-content">
                <div className="container">
                    <img src="Logo.png" className="img-thumbnail" alt="Cinque Terre" width="304" height="236"/>
                        <h2>H 2 Go</h2>
                        <p>Keep Hydrated by filling your reusable water
                            bottle .</p>
                </div>
            </div>
            <LoginPopup/>
        </div>
        </>
    )
}

export default Main;