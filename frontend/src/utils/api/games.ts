import { axiosInstance } from "./api"
import { Games } from "../../data/interfaces/games"
import { getHeaders } from "./api";

export async function getGames(): Promise<Games | undefined> {
    try{
        const config = getHeaders();
        const response = await axiosInstance.get("/games", config);
        if(response.status === 200){
            const player = response.data as Games;
            return player;
        }
        else return undefined
    }
    catch(error) {
        return undefined
    }
}