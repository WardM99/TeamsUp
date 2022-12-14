import { useEffect, useState } from "react";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Button from "react-bootstrap/Button";
import { Games } from "../../data/interfaces/games";
import { createGame, getGames } from "../../utils/api/games";
import GameCard from "./GameCard";

function GameList() {
  const [games, setGames] = useState<Games>();

  async function getGamesFromApi() {
    const response = await getGames();
    setGames(response);
  }

  async function createGameFromApi() {
    await createGame();
  }

  useEffect(() => {
    if (games === undefined) {
      getGamesFromApi();
    }
  });

  return (
    <Container data-testid="ListGamesId">
      <h1>GameList</h1>
      <Row>
        {games?.games.map((game, index) => {
          return (
            <Col key={`CardGame${game.gameId}`} xs={6}>
              <GameCard game={game} />
            </Col>
          );
        })}
      </Row>

      <Button
        data-testid="createNewGameButton"
        variant="primary"
        onClick={createGameFromApi}
      >
        Create New Game
      </Button>
    </Container>
  );
}

export default GameList;
