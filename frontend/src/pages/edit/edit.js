import React, {useEffect, useState} from "react";
import axiosInstance from "../../axios";
import styles from "../shop/shop.module.css";
import Navbar from "../../components/navbar";
import droplet from "../../assets/droplet.png";


const Edit = () => {
//get user info
    const [items, setItems] = useState(null);
    const [available,setAvailable] = useState(null);
    const [itemType, setItemType] = useState('Background');

    useEffect(() => {
        // Fetch items from backend based on current itemType
        console.log("Updating items: " + localStorage.getItem('access_token'));
        axiosInstance.get(`users/data`)
            .then(response => {
                console.log(response);
                setItems(response.data);
            })
            .catch(error => {
                console.error(error);
            });
    }, []);

    useEffect(() => {
        // Fetch available items from backend based on current itemType
        axiosInstance.get("/shop/auth-available/"+itemType+"/")
            .then(response => {
                console.log(response);
                setAvailable(response.data);
            })
            .catch(error => {
                console.error(error);
            });
    }, [itemType]);

    const handleItemClick = (item) => {
    };

    if(!items||!available){
        return (
            <div>
                Loading...
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

                </div>
                <div className={styles.items}>
                    {available.map((item, _) => (
                        <div key={item.name} className={styles.item} onDoubleClick={() => handleItemClick(item)}>
                            <img src={"http://"+item.image} alt={item.name} className={styles.itemImage} />
                            <div className={styles.itemPrice}>
                                <div className={styles.priceText}>
                                    {item.price}
                                </div>
                                <img src={droplet} className={styles.droplet}/>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )

}

export default Edit;