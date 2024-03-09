import axios from "axios";

export const Register = async (login, password, email, phone, receive) => {
    try {
        // const res = await axios.post(`${process.env.REACT_APP_API}/api/auth/login`, {
        //     username: login,
        //     password: password,
        //     email: email,
        //     phone: phone,
        //     receiveNotificationsEmail: receive
        // })
        console.log("TRUE")
        return 1
    }
    catch (error) {
        console.log(error)
    }
}