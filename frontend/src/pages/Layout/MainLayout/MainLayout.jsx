import React from 'react';
import {Outlet} from "react-router-dom";
import "./style.scss"
import Header from "../../../components/Header/Header";
import Background from "../../../components/bg/Background";

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