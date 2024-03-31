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
        if(login && password && email && phone) {
            console.log("TRUE")
            return 1
        }
        else {
            return alert("Не заполнены все поля")
        }

    }
    catch (error) {
        console.log(error)
    }
}