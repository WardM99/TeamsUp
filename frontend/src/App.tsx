import "./App.css";
import PlayersLogin from "./components/players/PlayersLogin";
import { Route, Routes } from "react-router-dom";
import Home from "./components/home/Home";
import PlayersCreate from "./components/players/PlayersCreate";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  return (
    <Routes>
      <Route path="/login" element={<PlayersLogin />} />
      <Route path="/register" element={<PlayersCreate />} />
      <Route path="/" element={<Home />} />
    </Routes>
  );
}

export default App;
