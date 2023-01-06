import { fireEvent, render, screen, waitFor } from "@testing-library/react";
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

describe('NavBar', () => {
    it("should render the component", async () => {
        render(<NavBar />);
        await waitFor(() => {
            const NavBarComponent = screen.getByTestId("NavBarId");
            const PlayersInfoComponent = screen.getByTestId("PlayersInfoId");
            const logoutButton = screen.getByTestId("LogOutButtonId");
            expect(NavBarComponent).toBeInTheDocument();
            expect(PlayersInfoComponent).toBeInTheDocument();
            expect(logoutButton).toBeInTheDocument();
        });
    });

    it("should logout and navigate to /login when logout is pressend", async () => {
        render(<NavBar />);
        await waitFor(() => {
            const logoutButton = screen.getByTestId("LogOutButtonId");
            fireEvent.click(logoutButton);
            expect(logout).toBeCalledTimes(1);
            expect(navigateMock).toBeCalledTimes(1);
            expect(navigateMock).toBeCalledWith("/login");
        });
    })
})