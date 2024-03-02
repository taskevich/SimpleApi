import React from 'react';
import string from "./../../string.json"
import {Link, NavLink} from "react-router-dom";
const MainPage = () => {
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
                    <div>
                        <button><Link to="auth">Авторизоваться</Link></button>
                        <button><Link to="reg">Зарегестрироваться</Link></button>
                    </div>
                </div>
            </header>
            <main></main>
            <footer>
                <p>Footer</p>
            </footer>
        </>
    )
};

export default MainPage;