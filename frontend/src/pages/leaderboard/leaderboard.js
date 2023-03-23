import React, {useEffect, useState} from 'react';

import classes from "./leaderboard.module.css";

import {Link, useLocation, useNavigate, useParams} from "react-router-dom";
import {render} from "react-dom";
import axiosInstance from "../../axios";
import FloorPlans from "../../components/floorPlans";
const Leaderboard = () => {
    // fetch top players for certain period , sorted by points
    //make button active or not depending on person location. Send a request to server that
    // will check if a user is close to geolocation or not
    const [leaders,setLeaders] = useState(null);
    const [error, setError] = useState(null);
    const [buttonText, setButtonText] = useState('Fill the bottle!');

    const {code} = useParams();

    const {state} = useLocation();

    const navigate = useNavigate();

    const handleClick = () => {
        const body = {building : code};
        axiosInstance.post('questions/auth',body)
            .then(response => {
                console.log(response.data);
                if(response.data.data.minutes) {
                    setButtonText(`You have ${response.data.data.minutes} min and ${response.data.data.seconds}s left`)
                    return;
                }
                console.log("Here go the");
                console.log(response.data);
                navigate("/quiz",{state:{location:code,questions:response.data.data}})
            })
            .catch(error => {
                console.error(error)
            })
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
                    {buttonText}
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
                    <div className={classes.first} style={{borderImage:`url(http://${leaders[0].border}) 360 repeat`,borderImageOutset: '5px'}}>
                        <div className={classes.userPic}>
                            <img src={'http://'+leaders[0].profile_pic} className={classes.userImg}/>
                        </div>
                        <Link to={`/profile/${leaders[0].username}`}><div className={classes.userName}>{leaders[0].username}</div></Link>
                        <div className={classes.points}> {leaders[0].points}</div>
                    </div>
                    {leaders.slice(1).map((leader, index) => (
                        <div className={classes.notFirst} style={{borderImage:`url(http://${leader.border}) 360 repeat`,borderImageOutset: '5px'}}>
                            <div className={classes.userPic}>
                                <img src={'http://'+leader.profile_pic} className={classes.userImg}/>
                            </div>
                            <Link to={`/profile/${leader.username}`}><div className={classes.userName}>{leader.username}</div></Link>
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
                <FloorPlans floors={state.floors}/>
            </div>
        </div>

    );

}

export default Leaderboard;