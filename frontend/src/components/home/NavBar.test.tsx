import { fireEvent, render, screen, waitFor, act } from "@testing-library/react";
import "@testing-library/jest-dom";
import NavBar from "./NavBar";
import { logout } from "../../utils/api/player";

jest.mock("../../utils/api/player", () => {
  return {
    logout: jest.fn(),
    currentPlayer: jest.fn().mockReturnValue({
      playerId: 1,
      name: "Jos",
    }),
  };
});

const navigateMock = jest.fn();

jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useNavigate: () => navigateMock,
}));

describe("NavBar", () => {
  it("should render the component", async () => {
    render(<NavBar />);
    const NavBarComponent = screen.getByTestId("NavBarId");
    const logoutButton = screen.getByTestId("LogOutButtonId");
    expect(NavBarComponent).toBeInTheDocument();
    expect(logoutButton).toBeInTheDocument();
    await waitFor(() => {
      const PlayersInfoComponent = screen.getByTestId("PlayersInfoId");
      expect(PlayersInfoComponent).toBeInTheDocument();
    });
  });
  it("should logout and navigate to /login when logout is pressend", async () => {
    render(<NavBar />);
    const logoutButton = screen.getByTestId("LogOutButtonId");
  
    act(() => {
      fireEvent.click(logoutButton);
    });
    expect(logout).toBeCalledTimes(1);
    expect(navigateMock).toBeCalledTimes(1);
    expect(navigateMock).toBeCalledWith("/login");
    
    await waitFor(() => { // Is only here so the test don't gives a warning
      const PlayersInfoComponent = screen.getByTestId("PlayersInfoId");
      expect(PlayersInfoComponent).toBeInTheDocument();
    });
  });
});
