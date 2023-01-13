import "./App.css";
import PlayersLogin from "./components/players/PlayersLogin";
import { Route, Routes } from "react-router-dom";
import Home from "./components/home/Home";
import PlayersCreate from "./components/players/PlayersCreate";
import "bootstrap/dist/css/bootstrap.min.css";
import GameLobby from "./components/games/GameLobby";
import NavBar from "./components/home/NavBar";

function App() {
  return (
    <>
      <NavBar />
      <Routes>
        <Route path="/login" element={<PlayersLogin />} />
        <Route path="/register" element={<PlayersCreate />} />
        <Route path="/" element={<Home />} />
        <Route path="/game/:gameId" element={<GameLobby /> } />
      </Routes>
    </>
  );
}

export default App;
