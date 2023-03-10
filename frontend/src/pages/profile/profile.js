import React from 'react';

import classes from "./profile.module.css";
import Navbar from "../../components/navbar";
import photo from "../../assets/useravatar.png";


const Profile = () => {

    //get list of achievements ,and whether they are completed or not
    //get user info

    return (
        <div className={classes.background}>
            <header>
                <Navbar />
            </header>
            <head>
                <title>User Profile</title>
                <link rel="stylesheet" href="style.css" />
            </head>
            <div className={classes.container}>
                <div className={classes.sidebar}>
                    <div className={classes.profile}>
                    <img className={classes.profileImg} src={photo} alt="Profile Picture of the user" />
                        <div className={classes.profileText}>
                        <h2>Username</h2>
                        <p>Full Name</p>
                        <p>Email</p>
                        <p>Course Title</p>
                        </div>
                    </div>
                </div>
                <div className={classes.main}>
                    <div className={classes.achievements}>
                        <h2 className={classes.achievements}>Achievements</h2>
                        <button className={classes.achievementButton}>
                            You filled your first water bottle!
                            <span className={classes.star1}></span>
                        </button>
                        <button className={classes.achievementButton}>
                            You filled water bottle 50 times!
                            <span className={classes.star2}></span>
                        </button>
                        <button className={classes.achievementButton}>
                            You are in top 10 on the leaderboard!
                            <span className={classes.star3}></span>
                        </button>
                    </div>   
                </div>
            </div>
        </div>    
    )
}

export default Profile;