import {API} from "../API/API";

export const Login = async (login, password) => {
    try{
        if(login && password) {
            const res = await API.post(`/api/auth/login`, {
                usernameOrEmail: login,
                password: password
            })
            console.log(res.data)
            return 1
        }
        else {
            console.log(false)
            return alert("Не заполнены поля")
        }
        // const res = await axios.post(`${process.env.REACT_APP_API}/api/auth/login`, {
        //     username: login,
        //     password: password
        // })


    }
    catch (error) {
        console.log(error)
    }
}