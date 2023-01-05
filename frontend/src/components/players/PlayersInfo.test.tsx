import { render, screen, waitFor } from "@testing-library/react";
import { currentPlayer } from "../../utils/api/player";
import PlayersInfo from "./PlayersInfo";

const navigateMock = jest.fn();

jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useNavigate: () => navigateMock,
}));

jest.mock("../../utils/api/player", () => {
  return {
    currentPlayer: jest
      .fn()
      .mockReturnValueOnce({
        playerId: 123,
        name: "John Doe",
      })
      .mockReturnValue(undefined),
  };
});

describe("PlayersInfo", () => {
  it("renders the player name when the player is logged in", async () => {
    render(<PlayersInfo />);
    expect(currentPlayer).toBeCalledTimes(1);
    await waitFor(() => {
      expect(screen.getByText("John Doe")).not.toBeUndefined();
    });
  });

  it("navigates to the login page when the player is not logged in", async () => {
    render(<PlayersInfo />);
    await waitFor(() => {
      expect(navigateMock).toBeCalledTimes(1);
    });
    await waitFor(() => {
      expect(navigateMock).toBeCalledWith("/login");
    });
  });
});
