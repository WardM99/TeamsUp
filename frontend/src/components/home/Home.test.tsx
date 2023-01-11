import { render, screen, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import { Games, Game } from "../../data/interfaces/games";
import Home from "./Home";

jest.mock("../../utils/api/player", () => {
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
    currentPlayer: jest.fn().mockReturnValue({
      playerId: 1,
      name: "Jos",
    }),
    getGames: jest.fn().mockReturnValue(games),
  };
});

const navigateMock = jest.fn();

jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useNavigate: () => navigateMock,
}));

describe("NavBar", () => {
  it("should render the component", async () => {
    render(<Home />);
    const NavBarComponent = screen.getByTestId("NavBarId");
    expect(NavBarComponent).toBeInTheDocument();
    const GameListComponent = screen.getByTestId("ListGamesId");
    expect(GameListComponent).toBeInTheDocument();
    await waitFor(() => {
      const PlayersInfoComponent = screen.getByTestId("PlayersInfoId");
      expect(PlayersInfoComponent).toBeInTheDocument();
    });
  });
});
