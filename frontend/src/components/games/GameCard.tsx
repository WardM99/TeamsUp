import { useState, FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import Modal from "react-bootstrap/Modal";
import Form from "react-bootstrap/Form";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrashCan } from "@fortawesome/free-solid-svg-icons";
import { IconProp } from "@fortawesome/fontawesome-svg-core";
import { Game } from "../../data/interfaces/games";
import { Team } from "../../data/interfaces/teams";

import { createTeam, joinTeam } from "../../utils/api/teams";

interface Props {
  game: Game;
  // handleClick: (edition: Edition) => Promise<void>;
}

function GameCard(props: Props) {
  const [show, setShow] = useState<boolean>(false);
  const [teamName, setTeamName] = useState("");
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const navigate = useNavigate();

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    handleClose();
    await createTeam(props.game.gameId, teamName);
  }

  async function joinTeamApi(teamId: number) {
    const team: Team | undefined = await joinTeam(props.game.gameId, teamId);
    if (team !== undefined) navigate(`/game/${props.game.gameId}`);
  }

  return (
    <>
      <Card data-testid={`GameCardId${props.game.gameId}`}>
        <Card.Header as="h5">
          Game of {props.game.owner.name}{" "}
          <Button variant="danger" className="float-end">
            <FontAwesomeIcon icon={faTrashCan as IconProp} />{" "}
          </Button>
        </Card.Header>
        <Card.Body>
          <Card.Title>Join a team</Card.Title>
          {props.game.teams.map((team, index) => {
            return (
              <Button
                key={`JoinTeam${team.teamId}`}
                onClick={() => joinTeamApi(team.teamId)}
              >{`Join ${team.teamName}`}</Button>
            );
          })}
        </Card.Body>
        <Card.Footer>
          <Button variant="success" onClick={handleShow}>
            Add Team
          </Button>
        </Card.Footer>
      </Card>
      <Modal
        show={show}
        onHide={handleClose}
        data-testid={`ModalToAddTeamGame${props.game.gameId}`}
      >
        <Modal.Header closeButton>
          <Modal.Title>Modal heading</Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSubmit}>
          <Modal.Body>
            <Form.Group controlId="formBasicTeamName">
              <Form.Label>Team name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter team name"
                onChange={(e) => setTeamName(e.target.value)}
                required
              />
            </Form.Group>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={handleClose}>
              Close
            </Button>
            <Button variant="primary" type="submit">
              Make Team
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>
    </>
  );
}

export default GameCard;
