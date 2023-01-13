import { render, screen, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import PlayersInfo from "./PlayersInfo";

const navigateMock = jest.fn();

jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useNavigate: () => navigateMock,
}));

describe("PlayersInfo", () => {
  it("renders the player name", async () => {
    render(<PlayersInfo playerName="John Doe" />);
    await waitFor(() => {
      expect(screen.getByText("John Doe")).toBeInTheDocument();
    });
  });
});
