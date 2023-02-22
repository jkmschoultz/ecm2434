import React from 'react';
import { useNavigate } from 'react-router-dom';
import classes from "./area.module.css";

import mockPhoto from "../assets/image 3.png";
const AreaPhoto = ({link,imgPath,type}) => {
    
    const navigate = useNavigate();

    const handleClick = () => {
      navigate(link);
    };

    return(<div className={classes.area} onClick={handleClick}>
        <img src={mockPhoto} className={classes.imageArea}></img>
    </div>)
}

export default AreaPhoto;