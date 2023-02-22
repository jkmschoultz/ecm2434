import React from 'react';

import classes from "./leaderboard.module.css";
import {useParams} from "react-router-dom";

const Leaderboard = () => {
    // fetch top players for certain period , sorted by points
    //make button active or not depending on person location. Send a request to server that
    // will check if a user is close to geolocation or not
    const {code} = useParams();

    return(
        <div className={classes.background}>
        <div className={classes.left}>
            <div className={classes.topDrinkers}>Top drinkers💦</div>
        </div>
        <div className={classes.right}>
            <div className={classes.logo}>{code}</div>
        </div>
        </div>

    )
}

export default Leaderboard;