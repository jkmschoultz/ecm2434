import React, { useState, useEffect } from 'react';
import Navbar from "../../components/navbar";
import styles from './shop.module.css';
import droplet from "../../assets/droplet.png";
import axiosInstance from "axios";
const Shop = () => {
    const [itemType, setItemType] = useState('backgrounds');
    const [selectedItem, setSelectedItem] = useState(null);
    const testItems = [
        {
            id: 1,
            name: 'Test Item 1',
            image: 'https://via.placeholder.com/150',
            price: '20'
        },
        {
            id: 2,
            name: 'Test Item 2',
            image: 'https://via.placeholder.com/150',
            price: '30'
        },
        {
            id: 3,
            name: 'Test Item 3',
            image: 'https://via.placeholder.com/150',
            price: '50'
        },
        {
            id: 4,
            name: 'Test Item 4',
            image: 'https://via.placeholder.com/150',
            price: '40'
        },
        {
            id: 5,
            name: 'Test Item 5',
            image: 'https://via.placeholder.com/150',
            price: '90'
        }
    ];
    const [items, setItems] = useState(testItems);

    const sendPurchaseRequest = (itemName) => {
        const body = { item_name: itemName };

        axiosInstance.post('/shop/auth-purchase', body)
            .then(response => {
                // Handle successful response here
            })
            .catch(error => {
                // Handle error here
                console.error('There was a problem with the purchase:', error);
            });
    };

    useEffect(() => {
        // Fetch items from backend based on current itemType
        fetch(`http://localhost:8000/shop/available`)
            .then(response => response.json())
            .then(data => setItems(data));
    }, [itemType]);

    const handleItemClick = (item) => {
        setSelectedItem(item);
    };

    const handlePopupClose = () => {
        setSelectedItem(null);
    };

    return (
        <div className={styles.background}>
            <Navbar></Navbar>
            <div className={styles.shop}>
                <div className={styles.itemTypes}>
                    <button onClick={() => setItemType('backgrounds')} className={itemType === 'backgrounds' ? styles.active : ''}>Backgrounds</button>
                    <button onClick={() => setItemType('borders')} className={itemType === 'borders' ? styles.active : ''}>Borders</button>
                    <button onClick={() => setItemType('profile-pictures')} className={itemType === 'profile-pictures' ? styles.active : ''}>Profile Pictures</button>
                </div>
                <div className={styles.items}>
                    {items.map((item, _) => (
                        <div key={item.name} className={styles.item} onClick={() => handleItemClick(item)}>
                            <img src={item.image} alt={item.name} className={styles.itemImage} />
                            <div className={styles.itemPrice}>
                                <div className={styles.priceText}>
                                    {item.price}
                                </div>
                                <img src={droplet} className={styles.droplet}/>
                            </div>
                        </div>
                    ))}
                </div>
                {selectedItem && (
                    <div className={styles.popup} onClick={handlePopupClose}>
                        <div className={styles.popupContent} onClick={(event) => event.stopPropagation()}>
                            <div className={styles.popupItem}>
                                <img src={selectedItem.image} alt={selectedItem.name} className={styles.itemImage}/>
                                <div className={styles.itemPrice}>
                                    <div className={styles.priceText}>
                                        {selectedItem.price}
                                    </div>
                                    <img src={droplet} className={styles.droplet}/>
                                </div>
                                <button onClick={sendPurchaseRequest(selectedItem.name)}>Purchase</button>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Shop;

