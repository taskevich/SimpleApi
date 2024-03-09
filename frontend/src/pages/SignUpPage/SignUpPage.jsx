import React, {useState} from 'react';
import {change} from "../../utils/lib/Change/Change";
import {useUser} from "../../utils/lib/Auth/UserContext";

const SignUpPage = () => {
    const {createUser} = useUser()
    const [user, setUser] = useState({
        login: "",
        password: "",
        email: "",
        phone: "",
        notifications: false
    })

    return(
        <>
            <h2>Регистрация</h2>
            <p>Логин</p>
            <input type="text" value={user.login} onChange={(e) => change(e, user, setUser)} name="login"/>
            <p>Email</p>
            <input type="email" value={user.email} onChange={(e) => change(e, user, setUser)} name="email"/>
            <p>Телефон</p>
            <input type="tel" value={user.phone} onChange={(e) => change(e, user, setUser)} name="phone"/>
            <p>Пароль</p>
            <input type="password" value={user.password} onChange={(e) => change(e, user, setUser)} name="password"/>
            <div className="notify flex">
                <input type="checkbox" value={user.notifications}
                       onChange={(e) => setUser({...user, notifications: !user.notifications})} name="notifications"/>
                <p>Рассылка</p>
            </div>

            <button onClick={() => createUser(user)} className="btn">
                Создать аккаунт
            </button>
        </>
    )
};

export default SignUpPage;