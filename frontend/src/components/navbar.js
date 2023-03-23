import React, { useState, useEffect } from 'react';
import Shop from "../pages/shop/shop";
import { Link } from "react-router-dom";
import classes from "./navbar.module.css";

import uniLogo from "../assets/uniLogo.svg";
import axiosInstance from '../axios';
import droplet from "../assets/droplet.png";

const Navbar = ({flag}) => {
    const [points, setPoints] = useState(0);

    //use effect on changes of flag to update the number of points dynamically
    useEffect(() => {
        // Fetch user data from backend
        axiosInstance.get(`users/data`)
            .then(response => {
                setPoints(response.data.points);
            })
            .catch(error => {
                console.error('There was a problem fetching user data:', error);
            });
    }, [flag]);

    return (
        <header className={classes.siteHeader}>
            <div>
                <ul id={classes.horizontalList}>
                    <li>
                        <Link to="/">
                            <img src={uniLogo} className={classes.imgArea} alt="logo" />
                        </Link>
                    </li>
                    <li>
                        <Link to="/location">
                            Location
                        </Link>
                    </li>
                    <li>
                        <Link to="/profile">
                            Profile
                        </Link>
                    </li>
                    <li>
                        <Link to="/shop">
                            Shop
                        </Link>
                    </li>
                    <li>
                        <div className={classes.points}>{points}<img src={droplet} className={classes.pointsDroplet}/></div>
                    </li>
                </ul>
            </div>
        </header>
    );
};

export default Navbar;
