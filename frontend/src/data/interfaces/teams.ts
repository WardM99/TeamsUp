import { Player } from "./player";

export interface Team {
    teamId: number;
    gameId: number;
    teamName: string;
    players: Player[];
}

export interface Teams {
    teams: Team[];
}