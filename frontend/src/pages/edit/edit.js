import React, {useEffect, useState} from "react";
import axiosInstance from "../../axios";
import Navbar from "../../components/navbar";
import droplet from "../../assets/droplet.png";

import styles from "./edit.module.css";

//This code contains a functional component named Edit which is used to edit user profile elements.
const Edit = () => {
    const [items, setItems] = useState(null);
    const [available,setAvailable] = useState(null);
    const [itemType, setItemType] = useState('Background'); //Initial type of item is Background

    useEffect(() => {
        // Fetch items from backend based on current itemType
        axiosInstance.get(`users/data`)
            .then(response => {
                console.log(response.data.profile_background);
                switch (itemType) { //switch because itemType is different at endpoint and json
                    case 'Background':
                        setItems(response.data.profile_background)
                        break;
                    case 'Profile Picture':
                        setItems(response.data.profile_pic)
                        break;
                    case 'Border':
                        setItems(response.data.profile_border)
                        break;
                }
            })
            .catch(error => {
                console.error(error);
            });
    }, [itemType]);

    useEffect(() => {
        // Fetch available items from backend based on current itemType
        axiosInstance.get("/shop/auth-owned/"+itemType+"/")
            .then(response => {
                console.log("Got an owned response")
                console.log(response);
                setAvailable(response.data.data);
            })
            .catch(error => {
                console.error(error);
            });
    }, [itemType]);

    //function to change chosen time of a chosen type
    const handleItemClick = (item) => {
        axiosInstance.get(`users/setPic/${item.name}/${item.item_type}/`)
            .then(response => {
                console.log("Changed Successfully to");
                console.log(item);
                setItems(item.image);
            })
            .catch(error => {
                console.error(error);
            })
    };

    //wait until json is ready
    if(!items||!available){
        return (
            <div>
                Loading... Saving turtles meanwhile...🐢🐢🐢
            </div>
        )
    }
    return(
        <div className={styles.background}>
            <Navbar flag={true}></Navbar>
            <div className={styles.profile}>
                <div className={styles.itemTypes}>
                    <button onClick={() => setItemType('Background')} className={itemType === 'Background' ? styles.active : ''}>Backgrounds</button>
                    <button onClick={() => setItemType('Border')} className={itemType === 'Border' ? styles.active : ''}>Borders</button>
                    <button onClick={() => setItemType('Profile Picture')} className={itemType === 'Profile Picture' ? styles.active : ''}>Profile Pictures</button>
                </div>
                <div className={styles.chosen}>
                    <div className={styles.item} className={styles.itemAvailable}>
                        <img src={"http://"+items} className={styles.itemImage} />
                        <div className={styles.blueAvailable}>
                            Equiped
                        </div>
                    </div>
                </div>
                <div className={styles.items}>
                    {available.map((item, _) => (
                        <div key={item.name} className={styles.item} onDoubleClick={() => handleItemClick(item)}>
                            <img src={"http://"+item.image} alt={item.name} className={styles.itemImage} />
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )

}

export default Edit;