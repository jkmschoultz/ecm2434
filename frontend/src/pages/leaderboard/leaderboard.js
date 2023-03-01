import React from 'react';

import classes from "./leaderboard.module.css";
import {useLocation, useNavigate, useParams} from "react-router-dom";
import {render} from "react-dom";
const Leaderboard = () => {
    // fetch top players for certain period , sorted by points
    //make button active or not depending on person location. Send a request to server that
    // will check if a user is close to geolocation or not
    const {code} = useParams();

    const {state} = useLocation();

    const navigate = useNavigate();
    const handleClick = () => {
        navigate("/quiz",{state:{location:code}})
    };
    let isAble;
    if (state.active) {
        isAble = (
            <div className={classes.containerButton} id="pnt">
                <button className={classes.pulseButton} onClick={handleClick}>
                    Fill the bottle!🚰
                </button>
            </div>
        );
    } else {
        isAble = (
            <div className={classes.container}>
                You are not at the required area!
            </div>
        );
    }

    return (
        <div className={classes.background}>
            <div className={classes.left}>
                <div className={classes.topDrinkers}>Top drinkers💦</div>
                {isAble}
            </div>
            <div className={classes.right}>
                <div className={classes.logo}>{code}</div>
            </div>
        </div>

    );

}

export default Leaderboard;