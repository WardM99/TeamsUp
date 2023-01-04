import axios from "axios"
import { axiosInstance } from "./api"
import { Games, Game } from "../../data/interfaces/games"
import { getHeaders } from "./api";

export async function getGames(): Promise<Games | undefined> {
    try{
        const config = getHeaders();
        const response = await axiosInstance.get("/games", config);
        const player = response.data as Games;
        return player;
    }
    catch(error) {
        return undefined
    }
}