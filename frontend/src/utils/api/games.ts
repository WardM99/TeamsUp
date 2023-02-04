import { axiosInstance, getHeaders } from "./api";
import { Games, Game } from "../../data/interfaces/games";

export async function getGames(): Promise<Games | undefined> {
  try {
    const config = getHeaders();
    const response = await axiosInstance.get("/games", config);
    if (response.status === 200) {
      const games = response.data as Games;
      return games;
    } else return undefined;
  } catch (error) {
    return undefined;
  }
}

export async function createGame(): Promise<Game | undefined> {
  try {
    const config = getHeaders();
    const response = await axiosInstance.post("/games", {}, config);
    if (response.status === 201) {
      const game = response.data as Game;
      return game;
    }
    return undefined;
  } catch (error) {
    return undefined;
  }
}

export async function nextStatus(gameId: Number): Promise<Number> {
  try {
    const config = getHeaders();
    const response = await axiosInstance.patch(`/games/${gameId}`, {}, config);
    return response.status;
  } catch (error) {
    return 500;
  }
}
