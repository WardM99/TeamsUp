import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrashCan } from "@fortawesome/free-solid-svg-icons";
import { IconProp } from "@fortawesome/fontawesome-svg-core";
import { Game } from "../../data/interfaces/games";

interface Props {
  game: Game;
  // handleClick: (edition: Edition) => Promise<void>;
}

function GameCard(props: Props) {
  return (
    <Card data-testid={`GameCardId${props.game.gameId}`}>
      <Card.Header as="h5">
        Game of {props.game.owner.name}{" "}
        <Button variant="danger" className="float-end">
          <FontAwesomeIcon icon={faTrashCan as IconProp} />{" "}
        </Button>
      </Card.Header>
      <Card.Body>
        <Card.Title>Join a team</Card.Title>
        <Button variant="primary">Join team 1</Button>{" "}
        <Button variant="primary">Join team 2</Button>
      </Card.Body>
    </Card>
  );
}

export default GameCard;
