import Button from "react-bootstrap/Button";
import GameList from "../components/games/GamesList";
import { Player } from '../data/interfaces/player';

interface Props {
    player: Player | undefined;
    isLoggedIn: boolean;
  }

function Homescreen(props: Props) {

    if(!props.isLoggedIn){
        return(
            <div>
                <Button variant="success" href="/login">
                    Login
                </Button>
                <Button href="/register">
                    Register
                </Button>
            </div>
        )
    }

    return (
        <GameList player={props.player}/>
    )
}

export default Homescreen