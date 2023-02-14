import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import GameComponent from "../components/games/states/GameComponent";
import GameLobby from "../components/games/states/GameLobby";
import { Player } from "../data/interfaces";
import { Game } from "../data/interfaces/games";
import { gameStatus } from "../utils/api/games";

interface Props {
    player: Player | undefined;
  }

function Gamescreen(props: Props) {
    const { gameId } = useParams();
    const [game, setGame] = useState<Game>();

    async function getGameApi() {
        const response = await gameStatus(Number(gameId));
        setGame(response);
      }
    useEffect(() => {
      getGameApi();
      // eslint-disable-next-line
    }, [gameId]);
    if(!game?.gameStarted){
        return(<GameLobby player={props.player} game={game}></GameLobby>)
    }

    return (
        <GameComponent player={props.player} game={game} />
    )
}

export default Gamescreen