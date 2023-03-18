
import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

const ProtectedRoute = () => {
    const isAuthenticated = () => {
        // Check if the user is authenticated, e.g., by checking the local storage for an access token
        const token = localStorage.getItem('access_token');
        return token !== null;
    };

    return isAuthenticated() ? <Outlet /> : <Navigate to="/register" />;
};

export default ProtectedRoute;
