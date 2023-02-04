import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Teams } from "../../../data/interfaces/teams";
import { getTeams, joinTeam } from "../../../utils/api/teams";
import { addCardToGame, getCards } from "../../../utils/api/cards";

import Card from "react-bootstrap/Card";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import ListGroup from "react-bootstrap/ListGroup";
import Carousel from "react-bootstrap/Carousel";
import { Button } from "react-bootstrap";
import { Player } from "../../../data/interfaces";
import { Cards } from "../../../data/interfaces/cards";
import { nextStatus } from "../../../utils/api/games";

interface Props {
  player: Player | undefined;
}

function GameLobby(props: Props) {
  const { gameId } = useParams();
  const [teams, setTeams] = useState<Teams>();
  const [cards, setCards] = useState<Cards>();

  async function getTeamsApi() {
    const response = await getTeams(Number(gameId));
    setTeams(response);
  }

  async function getCardsApi() {
    const response = await getCards();
    setCards(response);
  }

  useEffect(() => {
    if (teams === undefined) getTeamsApi();
    if (cards === undefined) getCardsApi();
  });
  return (
    <Container data-testid="GameLobby">
      <Row>
        {teams?.teams.map((team, index) => {
          const playersIdList = team?.players.map((player) => {
            return player.playerId;
          });
          const disabled =
            props.player !== undefined &&
            playersIdList.includes(props.player.playerId);
          return (
            <Col key={`TeamCardId${team.teamId}`} xs={6}>
              <Card data-testid={`TeamCardId${team.teamId}`}>
                <Card.Header>{team.teamName}</Card.Header>
                <Card.Body>
                  <Card.Title>Members</Card.Title>
                  <Card.Text>
                    <ListGroup>
                      {team?.players.map((player) => {
                        return (
                          <ListGroup.Item
                            key={`ListGroupItem${player.playerId}`}
                            data-testid={`ListGroupItem${player.playerId}`}
                          >
                            {player.name}
                          </ListGroup.Item>
                        );
                      })}
                    </ListGroup>
                  </Card.Text>
                </Card.Body>
                <Card.Footer>
                  <Button
                    variant="primary"
                    onClick={() => {
                      joinTeam(Number(gameId), team.teamId);
                    }}
                    disabled={disabled}
                  >
                    Join {team.teamName}
                  </Button>
                </Card.Footer>
              </Card>
            </Col>
          );
        })}
      </Row>
      <Row>
        <Col>
          <Button
            variant="success"
            onClick={() => {
              nextStatus(Number(gameId));
            }}
          >
            Start suggesting cards
          </Button>
        </Col>
      </Row>
      <Row>
        <Col>
          <Carousel variant="dark">
            {cards?.cards.map((card) => {
              return (
                <Carousel.Item>
                  <Card
                    key={`CardCardId${card.cardId}`}
                    className="text-center"
                  >
                    <Card.Body>
                      <Card.Title>{card.topic}</Card.Title>
                      <Card.Text>Points: {card.points}</Card.Text>
                      <Card.Footer>
                        <Button
                          onClick={() => {
                            addCardToGame(Number(gameId), card.cardId);
                          }}
                        >
                          Add
                        </Button>
                      </Card.Footer>
                    </Card.Body>
                  </Card>
                  <br />
                  <br />
                </Carousel.Item>
              );
            })}
          </Carousel>
        </Col>
      </Row>
    </Container>
  );
}

export default GameLobby;
