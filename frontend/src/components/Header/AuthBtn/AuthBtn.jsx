import React from 'react';
import Button from "../../../ui/Button/Button";
import NavButton from "../../../ui/NavButton/NavButton";
import {useUser} from "../../../utils/lib/Auth/UserContext";

const AuthBtn = () => {
    const {user, logout} = useUser()
    return (
        <div className="authBtn">
            {
                user != null ?
                    <>
                        <p>{user.login}</p>
                        <Button onClick={logout}>Выйти</Button>
                    </>
                    :
                    <>
                        <NavButton path="/panel/signin">Авторизоваться</NavButton>
                        <NavButton path="/panel/signup">Зарегестрироваться</NavButton>
                    </>
            }
        </div>
    )
};

export default AuthBtn;