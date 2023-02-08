import Card from "react-bootstrap/Card";
import Button from "react-bootstrap/Button";
import Carousel from "react-bootstrap/Carousel";
import { Cards } from "../../../data/interfaces/cards";
import { addCardToGame } from "../../../utils/api/cards";

interface Props {
  cards: Cards | undefined;
  gameId: number;
}

function CarouselComponent(props: Props) {
  if (props.cards === undefined) {
    return <div>Something went wrong</div>;
  }

  return (
    <Carousel variant="dark">
      {props.cards?.cards.map((card) => {
        return (
          <Carousel.Item key={`CarouselItem${card.cardId}`}>
            <Card key={`CardCardId${card.cardId}`} className="text-center">
              <Card.Body>
                <Card.Title>{card.topic}</Card.Title>
                <Card.Text>Points: {card.points}</Card.Text>
                <Card.Footer>
                  <Button
                    onClick={() => {
                      addCardToGame(props.gameId, card.cardId);
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
  );
}

export default CarouselComponent;
