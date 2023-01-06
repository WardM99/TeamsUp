import { useEffect, useState } from "react";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { Games } from "../../data/interfaces/games";
import { getGames } from "../../utils/api/games";
import GameCard from "./GameCard";

function GameList() {
  const [games, setGames] = useState<Games>();

  async function getGamesFromApi() {
    const response = await getGames();
    setGames(response);
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
    </Container>
  );
}

export default GameList;
