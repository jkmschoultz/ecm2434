import React, {useEffect, useState} from 'react';
import Navbar from '../../components/navbar';
import photo from '../../assets/useravatar.png';

import classes from './profile.module.css';
import axiosInstance from "../../axios";
import styles from "../shop/shop.module.css";
import droplet from "../../assets/droplet.png";
import editLogo from "../../assets/editLogo.png";
import {Link, useParams} from "react-router-dom";
import ProgressBar from "../../components/progressBar";

//page shows
const Profile = () => {
    //get list of achievements ,and whether they are completed or not
    //get user info
    const [items, setItems] = useState(null);
    const {userId} = useParams();

    useEffect(() => {
        if(userId) {
            axiosInstance.get(`users/${userId}`)
                .then(response => {
                    console.log(response);
                    setItems(response.data);
                })
                .catch(error => {
                    console.error(error);
                });
            return;
        }
        // Fetch items from backend based on current itemType
        console.log("Updating items: " + localStorage.getItem('access_token'));
        axiosInstance.get(`users/data`)
            .then(response => {
                setItems(response.data);
            })
            .catch(error => {
                console.error(error);
            });
    }, []);

    //wait until json is ready
    if(!items){
        return (
            <div>
                Loading... Saving turtles meanwhile...🐢🐢🐢
            </div>
        )
    }
    return (
        <div className={classes.background}>
            <header>
                <Navbar />
            </header>
            <div className={classes.container}>
                <div className={classes.sidebar} style={{borderImage:`url(http://${items.profile_border}) 20% repeat`}}>
                    <div className={classes.profile} style={{ background: `url(http://${items.profile_background})` , backgroundSize: 'cover', backgroundPosition: 'center' }}>
                        <div className={classes.profileImgContainer}>
                            <img className={classes.profileImg} src={"http://"+items.profile_pic} alt="Profile Picture of the user" />
                        </div>
                        <div className={classes.profileText}>
                            <h2>{items.username}</h2>
                            <div className={classes.quoteContainer}>
                                <h3>{`Level:${items.level}`}</h3>
                                <h3>{`Overall saved: ${items.bottles_filled} bottles🚰🚰🚰`}</h3>
                            </div>
                        </div>
                    </div>
                </div>
                <div className={classes.achievements}>
                    <h2>Achievements</h2>
                    <div className={classes.achievementContainer}>
                        {items.achievements.map((item, _) => (
                            <button className={`${classes.achievementButton} ${item.has ? classes.achievementButtonEarned : ''}`}>
                                <div className={classes.description}>
                                    <div className={classes.challengeName}>{item.name}</div>
                                    <div className={classes.challenge}>{item.challenge}</div>
                                </div>
                                <span className={`${classes.star} ${item.has ? classes.starAchieved : ''}`}></span>
                            </button>
                        ))}
                    </div>
                </div>
                {!userId && (
                    <Link to="/edit" className={classes.edit}><img src={editLogo} className={classes.editPhoto}></img></Link>
                    )}
            </div>
        </div>
    );
};

export default Profile;
