import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import GameCard from "./GameCard";
import { Game } from "../../data/interfaces/games";
import { Team } from "../../data/interfaces/teams";

const team1: Team = {
  teamId: 1,
  gameId: 2,
  teamName: "team 1",
  players: [],
};

const team2: Team = {
  teamId: 2,
  gameId: 2,
  teamName: "team 2",
  players: [],
};

const game: Game = {
  gameId: 2,
  roundOneDone: false,
  roundTwoDone: true,
  roundThreeDone: false,
  owner: {
    playerId: 3,
    name: "Jane",
  },
  teams: [team1, team2],
};

const navigateMock = jest.fn();
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useNavigate: () => navigateMock,
}));

describe("GameCard", () => {
  it("should display a card", () => {
    const props = {
      player: {
        playerId: 1,
        name: "Jos",
      },
      game,
    };
    render(<GameCard {...props} />);
    const gameCard = screen.getByTestId("GameCardId2");
    expect(gameCard).toBeInTheDocument();
  });

  it("should display the correct game owner name", () => {
    const props = {
      player: {
        playerId: 1,
        name: "Jos",
      },
      game,
    };
    render(<GameCard {...props} />);
    const gameOwnerName = screen.getByText("Game of " + game.owner.name);
    expect(gameOwnerName).toBeInTheDocument();
  });

  it("should contain a Card.Title element and two Button elements", async () => {
    const props = {
      player: {
        playerId: 1,
        name: "Jos",
      },
      game,
    };
    render(<GameCard {...props} />);
    const cardTitle = screen.getByText("Join a team");
    expect(cardTitle).toBeInTheDocument();
    const joinButton1 = screen.getByText("Join team 1");
    expect(joinButton1).toBeInTheDocument();
    const joinButton2 = screen.getByText("Join team 2");
    expect(joinButton2).toBeInTheDocument();
  });

  it("should contain a Button element with the correct variant and icon", () => {
    const props = {
      player: {
        playerId: 1,
        name: "Jos",
      },
      game,
    };
    render(<GameCard {...props} />);
    const deleteButton = screen.getAllByRole("button")[0];
    expect(deleteButton).toBeInTheDocument();
    expect(deleteButton.className).toEqual("float-end btn btn-danger");
  });
});
