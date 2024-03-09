import React, { createContext, useContext, useState } from 'react';
import {Login} from "./Login";
import {useNavigate} from "react-router";
import {Register} from "./Register";

const UserContext = createContext();

export const UserProvider = ({ children }) => {
    const nav = useNavigate()
    const [user, setUser] = useState(null);



    const login = (user) => {
        Login(user.username, user.password).then(res => {
            if(res === 1) {
                setUser(user)
                nav("/")
            }else {
                console.log("error")
            }
        })
    };

    const createUser = (user) => {
        console.log(user)
        Register(user.login, user.password, user.email, user.phone, user.notifications).then(res => {
            if (res === 1) {
                setUser(user)
                nav("/")
            }
            else {
                console.log("error")
            }
        })
    }


    const logout = () => {
        setUser(null);

    };

    return (
        <UserContext.Provider value={{user,login, createUser,logout }}>
            {children}
        </UserContext.Provider>
    );
};

export const useUser = () => useContext(UserContext);
