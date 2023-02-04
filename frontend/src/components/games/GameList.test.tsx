import { render, screen, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import GameList from "./GamesList";
import { Games, Game } from "../../data/interfaces/games";
import { getGames } from "../../utils/api/games";

jest.mock("../../utils/api/games", () => {
  const game1: Game = {
    gameId: 1,
    roundOneDone: true,
    roundTwoDone: false,
    roundThreeDone: false,
    owner: {
      playerId: 1,
      name: "Alice",
    },
    teams: [],
  };

  const game2: Game = {
    gameId: 2,
    roundOneDone: false,
    roundTwoDone: false,
    roundThreeDone: false,
    owner: {
      playerId: 2,
      name: "Bob",
    },
    teams: [],
  };
  const games: Games = {
    games: [game1, game2],
  };
  return {
    getGames: jest.fn().mockReturnValue(games),
  };
});

const navigateMock = jest.fn();
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useNavigate: () => navigateMock,
}));

describe("GameList", () => {
  it("should render a list of games", async () => {
    const props = {
      player: {
        playerId: 1,
        name: "Jos",
      },
    };
    render(<GameList {...props} />);
    expect(getGames).toBeCalledTimes(1);
    await waitFor(() => {
      const card1 = screen.getByTestId("GameCardId1");
      expect(card1).toBeInTheDocument();
    });
    await waitFor(() => {
      const card2 = screen.getByTestId("GameCardId2");
      expect(card2).toBeInTheDocument();
    });
  });
});
