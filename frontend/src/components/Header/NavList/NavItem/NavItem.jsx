import React from 'react';
import {NavLink} from "react-router-dom";

const NavItem = ({nav}) => {
    return (
        <NavLink className="navItem " to={nav.path}>{nav.title}</NavLink>
    )
};

export default NavItem;