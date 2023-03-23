import React, {useState} from "react";
import classes from "./floorPlans.module.css";

const FloorPlans = ({floors}) => {
    const [floor,setFloor] = useState(0);
    console.log(floors)
    return (
        <div className={classes.container}>
            <div className={classes.left}>
                <img src={'http://'+floors[floor].image} className={classes.floor}/>
            </div>
            <div className={classes.floorButtons}>
                {floors.map((photo,index) => (
                    <div key={photo.id} className={classes.choice} onClick={()=>setFloor(index)}>
                        {index}
                    </div>))}
            </div>
        </div>
    )
}

export default FloorPlans;