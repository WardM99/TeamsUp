import { render, screen, waitFor } from '@testing-library/react'
import GameList from './GamesList'
import { Games, Game } from '../../data/interfaces/games'
import { getGames } from '../../utils/api/games'

const game1: Game = {
    gameId: 1,
    roundOneDone: true,
    roundTwoDone: false,
    roundThreeDone: false,
    owner: {
      playerId: 1,
      name: 'Alice',
    }
}

const game2: Game = {
    gameId: 2,
    roundOneDone: false,
    roundTwoDone: false,
    roundThreeDone: false,
    owner: {
      playerId: 2,
      name: 'Bo b',
    },
}



jest.mock("../../utils/api/games", () =>{
  const game1: Game = {
    gameId: 1,
    roundOneDone: true,
    roundTwoDone: false,
    roundThreeDone: false,
    owner: {
      playerId: 1,
      name: 'Alice',
    }
}

const game2: Game = {
    gameId: 2,
    roundOneDone: false,
    roundTwoDone: false,
    roundThreeDone: false,
    owner: {
      playerId: 2,
      name: 'Bo b',
    },
}
const games: Games = {
  games: [game1, game2]
};
  return {
    getGames: jest.fn().mockReturnValue(games),
  };
});

describe('GameList', () => {
  it('should render a list of games',async () => {
    render(<GameList/>)
    expect(getGames).toBeCalledTimes(1);
    await waitFor(() => {
      const card1 = screen.getByTestId("GameCardId1");
      expect(card1).not.toBeUndefined();
    });
  })
});