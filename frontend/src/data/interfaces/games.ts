import { Player } from "./player";
import { Team } from "./teams";

export interface Game {
  gameId: number;
  roundOneDone: boolean;
  roundTwoDone: boolean;
  roundThreeDone: boolean;
  owner: Player;
  teams: Team[];
}

export interface Games {
  games: Game[];
}
