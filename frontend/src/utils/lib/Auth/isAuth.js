import axios from "axios";

export const isAuth = async (token, uid) => {
    try {

        if(token === "1") {
            console.log(1)
            const user = {
                login: "Admin"
            }
            return user
        }
        if (token === "2") {
            return 0
        }

    }
    catch (error) {
        console.log(error)
    }
}