import { useEffect, useState } from 'react'
import { Button, Card, Col, Container, Row } from 'react-bootstrap';
import { useParams } from 'react-router-dom';
import { Player } from '../../../data/interfaces';
import { Card as PlayCard } from '../../../data/interfaces/cards';
import { Game } from '../../../data/interfaces/games';
import { cardGuessed, getNextCard } from '../../../utils/api/cards';
import { getMyTurn } from '../../../utils/api/games';


interface Props {
    player: Player | undefined;
    game: Game | undefined;
  }
function GameComponent(props: Props) {
    const { gameId } = useParams();
    const [myTurn, setMyTurn] = useState<boolean>(false);
    const [myTurnText, setMyTurnText] = useState<string>("");
    const [currentCard, setCurrentCard] = useState<PlayCard>();

    async function getMyTurnApi(){
        const response = await getMyTurn(Number(gameId));
        setMyTurn(response);
        if(response){
            setMyTurnText("It's your turn");
        }
        else{
            setMyTurnText("It's not your turn");
        }
    }

    async function getNewCardApi(){
        const response = await getNextCard(Number(gameId));
        setCurrentCard(response);
    }

    async function cardGuessedApi() {
        if(currentCard !== undefined){
            const response = await cardGuessed(Number(gameId), currentCard.cardId);
            if(response === 200){
                getNewCardApi();
            }
        }
    }

    useEffect(() => {
        getMyTurnApi();
    // eslint-disable-next-line
    }, [gameId]);



  return (
    
    <Container data-testid="GameField">
        <Row>
            <Col>
                <span>{myTurnText}</span><br />
                <Button disabled={!myTurn}>Start Turn</Button>
                <Card key={`CardCardId${currentCard?.cardId}`} className="text-center" hidden={currentCard === undefined}>
                    <Card.Body>
                        <Card.Title>{currentCard?.topic}</Card.Title>
                        <Card.Text>Points: {currentCard?.points}</Card.Text>
                        <Card.Footer>
                        </Card.Footer>
                    </Card.Body>
                </Card>
                <Button variant='danger' onClick={getNewCardApi} hidden={currentCard === undefined}>Pass</Button>
                <Button variant='success' onClick={cardGuessedApi} hidden={currentCard === undefined}>Guessed</Button>
            </Col>
        </Row>
    </Container>
  )
}

export default GameComponent