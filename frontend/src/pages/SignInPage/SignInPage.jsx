import React, {useState} from 'react';
import {change} from "../../utils/lib/Change/Change";
import {useUser} from "../../utils/lib/Auth/UserContext";

const SignInPage = () => {
    const {login} = useUser()
    const [user, setUser] = useState({
        login: "",
        password: ""
    })


    return (
        <>
            <h2>Авторизация</h2>
            <p>Логин</p>
            <input value={user.login} onChange={(e) => change(e, user, setUser)} type="text" name="login"/>
            <p>Пароль</p>
            <input value={user.password} onChange={(e) => change(e, user, setUser)} type="password" name="password"/>
            <button className="btn" onClick={() => login(user)}>
                Войти
            </button>
        </>
    )
};

export default SignInPage;