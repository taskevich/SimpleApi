import React from 'react';
import string from "../../../string.json";
import {NavLink} from "react-router-dom";
import NavItem from "./NavItem/NavItem";

const NavList = () => {
    return (
        <li className="navList flex">
            {string.NavMenu.map((nav, index) => (
                <NavItem key={index} nav={nav}/>
            ))}
        </li>
    )
};

export default NavList;