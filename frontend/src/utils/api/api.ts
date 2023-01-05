import axios from "axios";
import { getAccessToken, getTokenType } from "../local-storage.ts/auth";

export const axiosInstance = axios.create();

axiosInstance.defaults.baseURL = "http://localhost:8000";

export function getHeaders() {
  const type = getTokenType();
  const token = getAccessToken();
  const config = {
    headers: {
      Authorization: `${type} ${token}`,
    },
  };
  return config;
}

/*
axiosInstance.interceptors.request.use(async config => {
    const accessToken = "test";
});
*/
