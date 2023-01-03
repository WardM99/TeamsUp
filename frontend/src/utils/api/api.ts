import axios from "axios"

export const axiosInstance = axios.create()

axiosInstance.defaults.baseURL = "http://localhost:8000"

/*
axiosInstance.interceptors.request.use(async config => {
    const accessToken = "test";
});
*/