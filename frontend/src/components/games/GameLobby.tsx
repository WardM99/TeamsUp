import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Teams } from "../../data/interfaces/teams";
import { getTeams, joinTeam } from "../../utils/api/teams";

import Card from "react-bootstrap/Card";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import ListGroup from "react-bootstrap/ListGroup";
import { Button } from "react-bootstrap";

function GameLobby() {
  const { gameId } = useParams();
  const [teams, setTeams] = useState<Teams>();

  async function getTeamsApi() {
    const response = await getTeams(Number(gameId));
    setTeams(response);
  }

  useEffect(() => {
    if (teams === undefined) getTeamsApi();
  });
  return (
    <Container data-testid="ListGamesId">
      <Row>
        {teams?.teams.map((team, index) => {
          return (
            <Col key={`TeamCardId${team.teamId}`} xs={6}>
              <Card data-testid={`TeamCardId${team.teamId}`}>
                <Card.Header>{team.teamName}</Card.Header>
                <Card.Body>
                  <Card.Title>Members</Card.Title>
                  <Card.Text>
                    <ListGroup>
                      {team?.players.map((player, index) => {
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
                      joinTeam(team.gameId, team.teamId);
                    }}
                  >
                    Join Team
                  </Button>
                </Card.Footer>
              </Card>
            </Col>
          );
        })}
      </Row>
    </Container>
  );
}

export default GameLobby;
