import React from "react";
import AuthBtn from "./AuthBtn/AuthBtn";
import LogoName from "./LogoName/LogoName";
import NavList from "./NavList/NavList";

const Header = () => {

    return(
        <header className="flex">
            <div className="flex container">
                <LogoName/>
                <NavList/>
                <AuthBtn/>
            </div>
        </header>
    )
};

export default Header;