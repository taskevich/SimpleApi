import axios from "axios";

export const API = axios.create({
    baseURL: process.env.REACT_APP_API,
    headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin" : "*"
    }
})