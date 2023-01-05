import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { currentPlayer } from "../../utils/api/player";
import { Player } from "../../data/interfaces";

function PlayersInfo() {
  const [player, setPlayer] = useState<Player>();
  const navigate = useNavigate();

  async function getPlayer() {
    const response = await currentPlayer();
    if (response === undefined) {
      navigate("/login");
    } else {
      setPlayer(response);
    }
  }

  useEffect(() => {
    if (player === undefined) getPlayer();
  });
  return <span>{player?.name}</span>;
}

export default PlayersInfo;
