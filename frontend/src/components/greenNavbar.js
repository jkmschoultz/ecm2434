import React from 'react';
import {Link} from "react-router-dom";
import "./greenNavbar.css";

import uniLogoWhite from "../assets/uniLogoWhite.png";

const greenNavbar = () => {

    return (
        <>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"/>
        <header>
            <div className="navbar-fixed-top" style={{backgroundColor: "#ededed"}}>
                <div className="container-fluid">
                    <div className="navbar-header">
                        <Link to="/" className="navbar-brand">
                            <img src={uniLogoWhite} width="120" alt="" className="d-inline-block align-middle mr-2"/>
                        </Link>
                        <button type="button" className="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
                            <span className="icon-bar"></span>
                            <span className="icon-bar"></span>
                            <span className="icon-bar"></span>
                        </button>
                        <Link className="navbar-brand" to="/"></Link>
                    </div>
                    <div className="collapse navbar-collapse" id="myNavbar">
                        <ul className="nav navbar-nav">
                            <li><Link to="/location">Location</Link></li>
                            <li><Link to="/profile">Profile</Link></li>
                        </ul>
                        <ul className="nav navbar-nav navbar-right">
                            <li className="signUp"> <Link to = "/register"><span className="glyphicon glyphicon-user"></span> Sign Up</Link> </li>
                        </ul>
                    </div>
                </div>
            </div>
        </header>
        </>
    )
}

export default greenNavbar;