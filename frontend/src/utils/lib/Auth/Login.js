import axios from "axios";

export const Login = async (login, password) => {
    try{
        // const res = await axios.post(`${process.env.REACT_APP_API}/api/auth/login`, {
        //     username: login,
        //     password: password
        // })

        console.log("TRUE")
        return 1
    }
    catch (error) {
        console.log(error)
    }
}