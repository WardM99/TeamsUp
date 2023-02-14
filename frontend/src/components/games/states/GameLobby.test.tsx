import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";
import GameLobby from "./GameLobby";
import { Team } from "../../../data/interfaces/teams";
import { Player } from "../../../data/interfaces";
import { getTeams, joinTeam } from "../../../utils/api/teams";
import { gameStatus, nextStatus } from "../../../utils/api/games";
import { Game } from "../../../data/interfaces/games";

const team1: Team = {
  teamId: 1,
  gameId: 2,
  teamName: "team 1",
  players: [],
};

const player: Player = {
  playerId: 1,
  name: "Jos",
};

const owner: Player = {
  playerId: 3,
  name: "Jane",
};

const team2: Team = {
  teamId: 2,
  gameId: 2,
  teamName: "team 2",
  players: [player],
};

const game: Game = {
  gameId: 2,
  maySuggestsCards: false,
  roundOneDone: false,
  roundTwoDone: false,
  roundThreeDone: false,
  gameStarted: false,
  owner,
  teams: [team1, team2],
};

jest.mock("../../../utils/api/teams", () => ({
  getTeams: jest.fn(() => Promise.resolve({ teams: [team1, team2] })),
  joinTeam: jest.fn(),
}));

jest.mock("../../../utils/api/cards", () => ({
  getCards: jest.fn(() => Promise.resolve({ cards: [] })),
  addCardToGame: jest.fn(),
}));

jest.mock("../../../utils/api/games", () => ({
  gameStatus: jest.fn(() => Promise.resolve(game)),
  nextStatus: jest.fn(),
}));

const props = {
  player,
  game,
};

describe("GameLobby", () => {
  beforeEach(() => {
    props.player = player;
  });
  it("should render the teams", async () => {
    render(<GameLobby {...props} />);
    expect(getTeams).toBeCalledTimes(1);
    await waitFor(() => {
      const card1 = screen.getByTestId("TeamCardId1");
      expect(card1).toBeInTheDocument();
    });
    await waitFor(() => {
      const card2 = screen.getByTestId("TeamCardId2");
      expect(card2).toBeInTheDocument();
    });
  });
  it("should have a disabled button when the player is already in the team", async () => {
    render(<GameLobby {...props} />);
    await waitFor(() => {
      const button = screen.getByText("Join team 2");
      expect(button).not.toBeEnabled();
    });
  });
  it("should have an enabled button when the player is already in the team", async () => {
    render(<GameLobby {...props} />);
    let button: HTMLElement;
    await waitFor(() => {
      button = screen.getByText("Join team 1");
      expect(button).toBeEnabled();
    }).then(() => {
      fireEvent.click(button);
      expect(joinTeam).toBeCalledTimes(1);
      // expect(joinTeam).toBeCalledWith(2,1)
    });
  });
  it("should verify that the nextStatus function is not called with the correct parameters when button is clicked", async () => {
    render(<GameLobby {...props} />);
    let button: HTMLElement;
    await waitFor(() => {
      button = screen.getByText("Start suggesting cards");
      expect(button).toBeInTheDocument();
    })
      .then(() => {
        expect(button).toBeDisabled();
      })
      .then(() => {
        fireEvent.click(button);
        expect(nextStatus).not.toBeCalled();
        // expect(nextStatus).toBeCalledWith(2);
      });
  });
  it("should verify that the nextStatus function is called with the correct parameters when button is clicked, maySuggestCards is false", async () => {
    props.player = owner;
    render(<GameLobby {...props} />);
    let button: HTMLElement;
    await waitFor(() => {
      button = screen.getByText("Start suggesting cards");
      expect(button).not.toBeDisabled();
    }).then(() => {
      fireEvent.click(button);
      expect(nextStatus).toBeCalledTimes(1);
      // expect(nextStatus).toBeCalledWith(2);
    });
  });
});
