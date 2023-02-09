import "./App.css";
import { useState, useEffect } from "react";
import PlayersLogin from "./components/players/PlayersLogin";
import { Route, Routes } from "react-router-dom";
import PlayersCreate from "./components/players/PlayersCreate";
import "bootstrap/dist/css/bootstrap.min.css";
import GameLobby from "./components/games/states/GameLobby";
import NavBar from "./components/home/NavBar";
import { Player } from "./data/interfaces";
import { currentPlayer } from "./utils/api/player";
import Homescreen from "./views/Homescreen";

function App() {
  const [player, setPlayer] = useState<Player>();
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);

  async function getPlayerApi() {
    const response = await currentPlayer();
    if (response !== undefined) {
      setPlayer(response);
      setIsLoggedIn(true);
    } else {
      // response failed
      setPlayer(undefined);
      setIsLoggedIn(false);
    }
  }

  useEffect(() => {
    getPlayerApi();
    // eslint-disable-next-line
  }, [isLoggedIn]);

  return (
    <>
      <NavBar
        player={player}
        isLoggedIn={isLoggedIn}
        setIsLoggedIn={setIsLoggedIn}
      />
      <Routes>
        <Route
          path="/login"
          element={<PlayersLogin setIsLoggedIn={setIsLoggedIn} />}
        />
        <Route
          path="/register"
          element={<PlayersCreate setIsLoggedIn={setIsLoggedIn} />}
        />
        <Route
          path="/"
          element={<Homescreen player={player} isLoggedIn={isLoggedIn} />}
        />
        <Route path="/game/:gameId" element={<GameLobby player={player} />} />
      </Routes>
    </>
  );
}

export default App;
