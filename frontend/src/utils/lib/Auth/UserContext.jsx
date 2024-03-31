import React, {createContext, useContext, useLayoutEffect, useState} from 'react';
import {Login} from "./Login";
import {useNavigate} from "react-router";
import {Register} from "./Register";
import {isAuth} from "./isAuth";




const UserContext = createContext();

export const UserProvider = ({ children }) => {
    const token = localStorage.getItem("token")
    const nav = useNavigate()
    const [user, setUser] = useState({
        login: null,
    });

    // const isauth = (token, userid) => {
    //     isAuth(token, userid).then(res => {
    //         if (res) {
    //             setUser(res)
    //         }
    //         if(res === 0) {
    //             console.log("error")
    //         }
    //     })
    // }
    // useLayoutEffect(() => {
    //     isauth(token, localStorage.getItem("uid"))
    //     console.log(user)
    // }, [token])
    const login = (user) => {
        Login(user.login, user.password).then(res => {
            if(res === 1) {
                setUser({login: user.login})
                localStorage.setItem("token", 1)
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
                setUser({login: user.login})
                localStorage.setItem("token", 2)
                nav("/")
            }
            else {
                console.log("error")
            }
        })
    }


    const logout = () => {
        localStorage.removeItem("token")
        setUser({login: null});

    };

    return (
        <UserContext.Provider value={{user,login, createUser,logout }}>
            {children}
        </UserContext.Provider>
    );
};

export const useUser = () => useContext(UserContext);
