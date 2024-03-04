import React from 'react';
import string from "../../string.json";
import {Link, NavLink, Outlet} from "react-router-dom";

const MainLayout = () => {
    return (
        <>
            <header className="flex">
                <div className="flex container">
                    <div className="logoName">
                        <h2>{string.NameProject}</h2>
                    </div>
                    <li className="navList flex">
                        {string.NavMenu.map((nav, index) => (
                            <NavLink className="navItem " key={index} to={nav.path}>{nav.title}</NavLink>
                        ))}
                    </li>
                    <div className="authBtn">
                        <button><Link to="/panel/signin">Авторизоваться</Link></button>
                        <button><Link to="/panel/signup">Зарегестрироваться</Link></button>
                    </div>
                </div>
            </header>
            <main>
                <Outlet/>
            </main>
            <footer>
                <p>Footer</p>
            </footer>
        </>
    )
};

export default MainLayout;