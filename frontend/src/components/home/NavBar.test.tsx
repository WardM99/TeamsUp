import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import NavBar from "./NavBar";
import { logout } from "../../utils/api/player";

jest.mock("../../utils/api/player", () => {
  return {
    logout: jest.fn(),
  };
});

const navigateMock = jest.fn();

jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useNavigate: () => navigateMock,
}));

describe("NavBar", () => {
  it("should render the component", async () => {
    const props = {
      player: {
        playerId: 1,
        name: "Jos",
      },
      isLoggedIn: true,
      setIsLoggedIn: jest.fn()
    }
    render(<NavBar {...props} />);
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
    const props = {
      player: {
        playerId: 1,
        name: "Jos",
      },
      isLoggedIn: true,
      setIsLoggedIn: jest.fn()
    }
    render(<NavBar {...props} />);
    const logoutButton = screen.getByTestId("LogOutButtonId");

    fireEvent.click(logoutButton);
    expect(logout).toBeCalledTimes(1);
    expect(props.setIsLoggedIn).toBeCalledWith(false);
    expect(navigateMock).toBeCalledTimes(1);
    expect(navigateMock).toBeCalledWith("/login");

    await waitFor(() => {
      // Is only here so the test don't gives a warning
      const PlayersInfoComponent = screen.getByTestId("PlayersInfoId");
      expect(PlayersInfoComponent).toBeInTheDocument();
    });
  });
});
