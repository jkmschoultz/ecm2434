import React, {useState} from "react";

import GreenNavbar from "../../components/greenNavbar";
import classes from "./register.module.css";
import {useNavigate} from "react-router-dom";
import axiosInstance from "../../axios";

//Shows register page and handles the form
const Register = () => {

    const navigate = useNavigate();
    const initialFormData = Object.freeze({
        email : '',
        username :'',
        password: ''
    });

    const [formData, updateFormData] = useState(initialFormData);

    const handleChange = (e) => {
        updateFormData({
            ...formData,
            [e.target.name]: e.target.value.trim(),
        });
        console.log(formData);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("I am posting this");
        console.log(formData);
        localStorage.setItem('access_token',"Bearer ");
        axiosInstance
            .post(`auth/register`, {
                email: formData.email,
                username: formData.username,
                password: formData.password,
            })
            .then((res) => {
                navigate('/');
                console.log(res);
                console.log(res.data);
            });
    };

    const disabled = () => {
        if(formData.password) {
            return ( !(formData.password == formData.pswrepeat))
        }
        return true
    }
    return (
        <>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"/>
            <GreenNavbar></GreenNavbar>
            <main>
                <div className="container-fluid p-0">
                    <div className="site-content">
                        <div className={classes.container}>
                            <form className={classes.form}  method="post">
                                <h1 className="login-title">Registration</h1>
                                        <label htmlFor='email'><b>Email</b></label>
                                        <input type='text' placeholder='Enter email' name='email' onChange={handleChange} required/>
                                        <label htmlFor="username"><b>Username</b></label>
                                        <input type="text" placeholder="Enter Username" name="username" id="use" onChange={handleChange} required/>
                                            <label htmlFor="psw"><b>Password</b></label>
                                            <input type="password" placeholder="Enter Password" name="password" id="password" onChange={handleChange} required/>
                                                <label htmlFor="psw-repeat"><b>Repeat Password</b></label>
                                                <input type="password" placeholder="Repeat Password" name="pswrepeat"
                                                       id="pswrepeat" onChange={handleChange} required/>
                                                    <button type="submit" className="signupbtn" name="submit" disabled={disabled()} onClick={handleSubmit}>Register</button>
                            </form>
                        </div>
                    </div>
                </div>


            </main>
        </>
    )
}

export default Register;