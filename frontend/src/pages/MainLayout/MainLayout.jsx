import React from 'react';
import string from "../../string.json";
import {Link, NavLink, Outlet} from "react-router-dom";
import {useUser} from "../../utils/lib/Auth/UserContext";
import "./style.scss"
import Header from "../../components/Header/Header";
import Background from "../../components/bg/Background";

const MainLayout = () => {
    return (
        <>
            <Header/>
            <main className="flex">
                <div className="container">
                    <Outlet/>
                </div>
            </main>
            <footer className="flex">
                <div className="container">
                    <p>Footer</p>
                </div>
            </footer>

            <Background/>
        </>
    )
};

export default MainLayout;