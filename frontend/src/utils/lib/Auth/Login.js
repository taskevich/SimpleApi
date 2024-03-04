import axios from "axios";

export const Login = async (login, password) => {
    try{
        const res = await axios.post(`${process.env.REACT_APP_API}/api/auth/login`, {
            login,
            password
        })
        console.log("TRUE")
        return res
    }
    catch (error) {
        console.log(error)
    }
}