import { Player } from "./player";

export interface Game {
    gameId: number;
    roundOneDone: boolean;
    roundTwoDone: boolean;
    roundThreeDone: boolean
    owner: Player
}

export interface Games {
    games: [Game]
}