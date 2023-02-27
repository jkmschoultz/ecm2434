import React from 'react';

import classes from "./progressBar.module.css";
const ProgressBar = ({currentPoints,maxPoints}) => {

    const percentage = Math.round((currentPoints / maxPoints) * 100);

    return (
        <div className={classes.progressBar}>
            <div className={classes.progressBarFill} style={{ width: `${percentage}%` }}>
            </div>
        </div>
    );
}

export default ProgressBar;