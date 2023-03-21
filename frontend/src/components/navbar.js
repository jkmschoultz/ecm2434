import React, { useState, useEffect } from 'react';
import { Link } from "react-router-dom";
import classes from "./navbar.module.css";

import uniLogo from "../assets/uniLogo.svg";
import axiosInstance from '../axiosInstance';

const Navbar = () => {
    const [points, setPoints] = useState(0);

    useEffect(() => {
        // Fetch user data from backend
        axiosInstance.get('user')
            .then(response => {
                setPoints(response.data.points);
            })
            .catch(error => {
                console.error('There was a problem fetching user data:', error);
            });
    }, []);

    const handlePurchaseSuccess = (itemName, price) => {
        // Make a post request to update the user balance
        const body = { item_name: itemName, price: price };
        axiosInstance.post('/shop/auth-purchase', body)
            .then(response => {
                // Update the balance in the navbar
                setPoints(response.data.points);
            })
            .catch(error => {
                console.error('There was a problem with the purchase:', error);
            });
    };

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
                        {/* Pass the handlePurchaseSuccess function as a prop to the Shop component */}
                        <Shop onPurchaseSuccess={handlePurchaseSuccess} />
                    </li>
                    <li>
                        <div className={classes.points}>{points} droplets</div>
                    </li>
                </ul>
            </div>
        </header>
    );
};

export default Navbar;
