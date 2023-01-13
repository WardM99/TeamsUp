import React from 'react'
import { useParams } from 'react-router-dom'

function GameLobby() {
    const { gameId } = useParams();
  return (
    <div>GameLobby {gameId}</div>
  )
}

export default GameLobby