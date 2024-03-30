import React from 'react';
import {Outlet} from "react-router-dom";
import "./style.scss";
import Background from "../../../components/bg/Background";

const AuthLayout = () => {
    return(
        <>
            <div className="window flex">
                <div className="authForm flex">
                    <Outlet/>
                </div>
            </div>
            <Background/>
        </>
    )
};

export default AuthLayout;