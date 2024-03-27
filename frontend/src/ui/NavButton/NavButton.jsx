import React from 'react';
import {Link} from "react-router-dom";
import "./style.scss"

const NavButton = ({children, path}) => {
    return (
        <Link className="btn" to={path}>{children}</Link>
    )
};

export default NavButton;