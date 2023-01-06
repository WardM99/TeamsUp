import { render } from '@testing-library/react';
import GameCard from './GameCard';
import { Game } from '../../data/interfaces/games';

const game: Game = {
    gameId: 2,
    roundOneDone: false,
    roundTwoDone: true,
    roundThreeDone: false,
    owner: {
      playerId: 3,
      name: 'Jane',
    },
};


describe('GameCard', () => {
  
      
    it('should display the correct game owner name', () => {
        const { getByText } = render(<GameCard game={game} />);
        const gameOwnerName = getByText("Game of "+game.owner.name);
        expect(gameOwnerName).not.toBeUndefined();
    });

    it('should contain a Card.Title element and two Button elements', () => {
        const { getByText } = render(<GameCard game={game} />);
        const cardTitle = getByText('Join a team');
        const joinButton1 = getByText('Join team 1');
        const joinButton2 = getByText('Join team 2');
        console.log(cardTitle)
        expect(cardTitle).not.toBeUndefined();
        expect(joinButton1).not.toBeUndefined();
        expect(joinButton2).not.toBeUndefined();
    });
    
    it('should contain a Button element with the correct variant and icon', () => {
        const { getAllByRole } = render(<GameCard game={game} />);
        const deleteButton = getAllByRole("button")[0];
        expect(deleteButton.className).toEqual("float-end btn btn-danger")
    });
});
