import React from 'react';
import {Link} from "react-router-dom";
import classes from "./navbar.module.css";

import uniLogo from "../assets/uniLogo.svg";

const Navbar = () => {
    
    return (
        <header className={classes.siteHeader}>
            <div>
                <ul id = {classes.horizontalList}>
                    <li>
                    <Link to="/">
                        <img src={uniLogo} className = {classes.imgArea} alt="logo"/>
                    </Link>
                    </li>
                    <li>
                        <Link to= "/location">
                            Location
                        </Link>
                    </li>
                    <li>
                        <Link to="/profile">
                            Profile
                        </Link>
                    </li>
                </ul>
            </div>
        </header>
    )
}

export default Navbar;