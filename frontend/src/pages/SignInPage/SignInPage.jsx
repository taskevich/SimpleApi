import React, {useState} from 'react';
import {Login} from "../../utils/lib/Auth/Login";

const SignInPage = () => {
    const [user, setUser] = useState({
        login: "",
        password: ""
    })
    const changed = (e) => {
        const {name, value} = e.target
        setUser({...user,[name]:value})
    }
    return (
        <div>
            <input value={user.login} onChange={changed} type="text" name="login"/>
            <input value={user.password} onChange={changed} type="text" name="password"/>
            <button onClick={() =>Login(user.login, user.password)}>
                Войти
            </button>
        </div>
    )
};

export default SignInPage;