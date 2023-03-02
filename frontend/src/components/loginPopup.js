import React, { useState } from 'react';
import "./loginPopup.css";
import {Link, useNavigate} from "react-router-dom";
import axiosInstance from "../axios";

const LoginPopup= () =>  {
    const [formVisible, setFormVisible] = useState(false);

    const initialFormData = Object.freeze({
        username : '',
        password: '',
    });

    const [formData, updateFormData] = useState(initialFormData);

    const navigate = useNavigate();
    const handleChange = (e) => {
        updateFormData({
            ...formData,
            [e.target.name]: e.target.value.trim(),
        });
        console.log(formData);
    };


    const openForm = () => {
        setFormVisible(true);
        console.log(formVisible)
    };

    const closeForm = () => {
        setFormVisible(false);
    };


    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(formData);

        axiosInstance
            .post(`/auth/token`, {
                username: formData.username ,
                password: formData.password,
            })
            .then((res) => {
                localStorage.setItem('access_token', res.data.access);
                localStorage.setItem('refresh_token', res.data.refresh);
                axiosInstance.defaults.headers['Authorization'] =
                    'JWT ' + localStorage.getItem('access_token');
                navigate("/location");
                //console.log(res);
                //console.log(res.data);
            });
    };

    return (
        <>
            <button className="open-button" onClick={openForm}>Login</button>
            {formVisible && (
                <div className="form-popup" id="myForm">
                    <form onSubmit={handleSubmit} className="form-container">
                        <h1>Login</h1>

                        <label htmlFor="username"><b>Username</b></label>
                        <input type="text" placeholder="Enter Username" name="username" onChange={handleChange} required/>

                        <label htmlFor="password"><b>Password</b></label>
                        <input type="password" placeholder="Enter Password" name="password" onChange={handleChange} required  />

                        <button type="submit">Login</button>
                        <label>
                            <p>Don’t have a user account? <Link to ="/register" className="registerText">Register now</Link></p>
                        </label>
                        <button type="button" className="btn cancel" onClick={closeForm}>Close</button>
                    </form>
                </div>
            )}
        </>
    );
}

export default LoginPopup;
