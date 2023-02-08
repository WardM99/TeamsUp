import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Teams } from "../../../data/interfaces/teams";
import { getTeams, joinTeam } from "../../../utils/api/teams";
import { getCards } from "../../../utils/api/cards";

import Card from "react-bootstrap/Card";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import ListGroup from "react-bootstrap/ListGroup";
import { Button } from "react-bootstrap";
import { Player } from "../../../data/interfaces";
import { Cards } from "../../../data/interfaces/cards";
import { gameStatus, nextStatus } from "../../../utils/api/games";
import CarouselComponent from "./CarouselComponent";
import { Game } from "../../../data/interfaces/games";

interface Props {
  player: Player | undefined;
}

function GameLobby(props: Props) {
  const { gameId } = useParams();
  const [teams, setTeams] = useState<Teams>();
  const [cards, setCards] = useState<Cards>();
  const [game, setGame] = useState<Game>();
  const [buttonText, setButtonText] = useState<string>("Start suggesting Cards");
  const [buttonDisabled, setButtonDisabled] = useState<boolean>(true);

  if(game !== undefined && game.owner.playerId === props.player?.playerId && buttonDisabled){
    setButtonDisabled(false);
  }

  if(game !== undefined && game.maySuggestsCards && buttonText !== "Start game"){
    setButtonText("Start game");
  }

  async function getTeamsApi() {
    const response = await getTeams(Number(gameId));
    setTeams(response);
  }

  async function getCardsApi() {
    const response = await getCards();
    setCards(response);
  }

  async function getGameApi() {
    const response = await gameStatus(Number(gameId));
    setGame(response);
  }
  useEffect(() => {
    getTeamsApi();
    getCardsApi();
    getGameApi();
    console.log("TEST");
    // eslint-disable-next-line
  }, [gameId]);
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
            disabled={buttonDisabled}
          >
            {buttonText}
          </Button>
        </Col>
      </Row>
      <Row>
        <Col>
          <CarouselComponent cards={cards} gameId={Number(gameId)} />
        </Col>
      </Row>
    </Container>
  );
}

export default GameLobby;
