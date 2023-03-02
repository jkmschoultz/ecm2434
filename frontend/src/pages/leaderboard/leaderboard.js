import React, {useEffect, useState} from 'react';

import classes from "./leaderboard.module.css";

import {useLocation, useNavigate, useParams} from "react-router-dom";
import {render} from "react-dom";
const Leaderboard = () => {
    // fetch top players for certain period , sorted by points
    //make button active or not depending on person location. Send a request to server that
    // will check if a user is close to geolocation or not
    const [leaders,setLeaders] = useState(null);
    const [error, setError] = useState(null);

    const {code} = useParams();

    const {state} = useLocation();

    const navigate = useNavigate();

    const handleClick = () => {
        navigate("/quiz",{state:{location:code}})
    };

    useEffect( () => {
        const fetchData = async () => {
            try {
                const response = await fetch('http://localhost:8000/leaderboard/'+code, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                const responseData = await response.json();
                console.log(responseData);
                let changedData = responseData.data;
                setLeaders(changedData);
            }
            catch (error) {
                setError(error);
            }
        }
        fetchData();
    }, []);


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

    let getLeaders;

    if (!leaders) {
        getLeaders = (
            <div className={classes.leadersList}>
                <div className={classes.fail}> Sorry , wait for leaders to download </div>
            </div>
        )
    } else {
        if(leaders.length == 0) {
            getLeaders = (
                <div className={classes.leadersList}>
                    <div className={classes.fail}>There are no contestants. Be first!</div>
                </div>
            )
        }
        else {
            getLeaders = (
                <div className={classes.leadersList}>
                    <div className={classes.first}>
                        <div className={classes.userName}>{leaders[0].username}</div>
                        <div className={classes.points}> {leaders[0].points}</div>
                    </div>
                    {leaders.slice(1).map((leader, index) => (
                        <div className={classes.notFirst}>
                            <div className={classes.userName}>{leader.username}</div>
                            <div className={classes.points}> {leader.points}</div>
                        </div>
                    ))}
                </div>
            )
        }
    }

    return (
        <div className={classes.background}>
            <div className={classes.left}>
                <div className={classes.topDrinkers}>Top drinkers💦</div>
                {getLeaders}
                {isAble}
            </div>
            <div className={classes.right}>
                <div className={classes.logo}>{code}</div>
            </div>
        </div>

    );

}

export default Leaderboard;