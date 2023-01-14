import "./App.css";
import { useState, useEffect } from "react";
import PlayersLogin from "./components/players/PlayersLogin";
import { Route, Routes, useNavigate } from "react-router-dom";
import Home from "./components/home/Home";
import PlayersCreate from "./components/players/PlayersCreate";
import "bootstrap/dist/css/bootstrap.min.css";
import GameLobby from "./components/games/GameLobby";
import NavBar from "./components/home/NavBar";
import { Player } from "./data/interfaces";
import { currentPlayer } from "./utils/api/player";

function App() {
  const [player, setPlayer] = useState<Player>();
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);

  const navigate = useNavigate();

  async function getPlayerApi() {
    if (player === undefined) {
      const response = await currentPlayer();
      if (response !== undefined) {
        setPlayer(response);
        setIsLoggedIn(true);
      }
    } else {
      const response = await currentPlayer();
      if (response === undefined) {
        setIsLoggedIn(false);
      } else if (response.playerId !== player.playerId) {
        setPlayer(response);
        setIsLoggedIn(true);
        navigate("/");
      }
    }
  }

  useEffect(() => {
    getPlayerApi();
  });

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
        <Route path="/" element={<Home />} />
        <Route path="/game/:gameId" element={<GameLobby />} />
      </Routes>
    </>
  );
}

export default App;
