import string from "../../string.json";
import {Link, NavLink} from "react-router-dom";
import React from "react";
import {useUser} from "../../utils/lib/Auth/UserContext";

const Header = () => {
    const {user, logout} = useUser()
    return(
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
                    {
                        user != null ?
                            <>
                                <p>{user.login}</p>
                                <button className="btn" onClick={() => logout()}>Выйти</button>
                            </>

                            :
                            <>
                                <Link className="btn" to="/panel/signin">Авторизоваться</Link>
                                <Link className="btn" to="/panel/signup">Зарегестрироваться</Link>
                            </>
                    }

                </div>
            </div>
        </header>
    )
};

export default Header;