import React from 'react';
import classes from "./main.css";
import GreenNavbar from "../../components/greenNavbar";
import LoginPopup from "../../components/loginPopup";
import Logo from "../../assets/Logo.png";

const Main = () => {
    return (
        <>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"/>
        <GreenNavbar />
        <div className="container-fluid p-0">
            <div className="site-content">
                <div className="container">
                    <img src={Logo} className="img-thumbnail" alt="Logo" width="304" height="236" />
                    <h2>H2 GO</h2>
                    <p>STAY HYDRATED BY REFILLING  YOUR REUSABLE WATER BOTTLE.</p>
                </div>
            </div>
            <LoginPopup />
        </div>
        </>
    )
}

export default Main;
