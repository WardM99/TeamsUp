import axios from "axios"
import { axiosInstance } from "./api"
import { Player } from "../../data/interfaces";
import { setAccessToken, setTokenType } from "../local-storage.ts/auth"
import { getHeaders } from "./api";


interface LoginResponse {
    access_token: string;
    token_type: string;
    user: Player;
}

function setLogInTokens(response: LoginResponse) {
    setAccessToken(response.access_token);
    setTokenType(response.token_type);
}


export async function createPlayer(name: string, password: string) : Promise<number> {
    const payload = {
        "name": name,
        "password": password,
    }
    try{
        const response = await axiosInstance.post("/players", payload);
        const login = response.data as LoginResponse
        //setLogInTokens(login);
        return response.status;
    }
    catch (error) {
        if (axios.isAxiosError(error)) {
            return error.response?.status || 500;
        } else {
            return 500;
        }
    }
}

export async function login(name: string, password: string): Promise<number> {
    const payload = new FormData();
    payload.append("username", name);
    payload.append("password", password);
    try{
        const response = await axiosInstance.post("/players/login", payload);
        const login = response.data as LoginResponse
        setLogInTokens(login);
        return response.status;
    }
    catch (error) {
        if (axios.isAxiosError(error)) {
            return error.response?.status || 500;
        } else {
            return 500
        }
    }
}


export function logout() : void {
    setAccessToken(null);
    setTokenType(null);
}

export async function currentPlayer(): Promise<Player | undefined> {
    try{
        const config = getHeaders();
        const response = await axiosInstance.get("/players/current", config);
        const player = response.data as Player;
        return player;

    }
    catch(error) {
        return undefined;
    }
}