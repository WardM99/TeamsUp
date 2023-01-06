import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import GameCard from "./GameCard";
import { Game } from "../../data/interfaces/games";

const game: Game = {
  gameId: 2,
  roundOneDone: false,
  roundTwoDone: true,
  roundThreeDone: false,
  owner: {
    playerId: 3,
    name: "Jane",
  },
};

describe("GameCard", () => {
  it("should display a card", () => {
    render(<GameCard game={game} />);
    const gameCard = screen.getByTestId("GameCardId2");
    expect(gameCard).toBeInTheDocument();
  });

  it("should display the correct game owner name", () => {
    render(<GameCard game={game} />);
    const gameOwnerName = screen.getByText("Game of " + game.owner.name);
    expect(gameOwnerName).toBeInTheDocument();
  });

  it("should contain a Card.Title element and two Button elements", () => {
    render(<GameCard game={game} />);
    const cardTitle = screen.getByText("Join a team");
    const joinButton1 = screen.getByText("Join team 1");
    const joinButton2 = screen.getByText("Join team 2");
    expect(cardTitle).toBeInTheDocument();
    expect(joinButton1).toBeInTheDocument();
    expect(joinButton2).toBeInTheDocument();
  });

  it("should contain a Button element with the correct variant and icon", () => {
    render(<GameCard game={game} />);
    const deleteButton = screen.getAllByRole("button")[0];
    expect(deleteButton).toBeInTheDocument();
    expect(deleteButton.className).toEqual("float-end btn btn-danger");
  });
});
