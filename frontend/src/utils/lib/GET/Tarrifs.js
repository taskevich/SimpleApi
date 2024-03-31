
import {API} from "../API/API";

export const TarifsGet = async () => {
    try {
        const list = await API.get(`/api/tariffs`, {
            headers: {
                "Content-Type" : "application/json"
            }
        })
        return list.data
    }
    catch (error) {
        console.log(error)
    }
}