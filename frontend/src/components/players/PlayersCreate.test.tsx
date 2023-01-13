import { render, fireEvent, screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import PlayersCreate from "./PlayersCreate";
import { createPlayer } from "../../utils/api/player";

const navigateMock = jest.fn();

jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useNavigate: () => navigateMock,
}));

jest.mock("../../utils/api/player", () => {
  return {
    createPlayer: jest
      .fn()
      .mockImplementation((name: string, password: string) => {
        if (name === "testuser" && password === "testpassword") return 201;
        return 400;
      }),
  };
});

describe("PlayersCreate", () => {
  it("there is a nameInput, passwordInput, loginButton and createButton", async () => {
    render(<PlayersCreate setIsLoggedIn={jest.fn()}></PlayersCreate>);
    const nameInput = screen.getByLabelText("Name");
    const passwordInput = screen.getByLabelText("Password");
    const loginButton = screen.getByText("Login");
    const createButton = screen.getByText("Create");

    expect(nameInput).toBeInTheDocument();
    expect(passwordInput).toBeInTheDocument();
    expect(loginButton).toBeInTheDocument();
    expect(createButton).toBeInTheDocument();
  });

  it("form submission calls createPlayer function with correct arguments", async () => {
    const setIsLoggedIn = jest.fn();
    render(<PlayersCreate setIsLoggedIn={setIsLoggedIn}></PlayersCreate>);
    const nameInput = screen.getByLabelText("Name");
    const passwordInput = screen.getByLabelText("Password");
    const createButton = screen.getByText("Create");

    fireEvent.change(nameInput, { target: { value: "testuser" } });
    fireEvent.change(passwordInput, { target: { value: "testpassword" } });
    await fireEvent.click(createButton);

    expect(createPlayer).toBeCalledTimes(1);
    expect(createPlayer).toBeCalledWith("testuser", "testpassword");
    expect(setIsLoggedIn).toBeCalledWith(true);
    expect(navigateMock).toBeCalledTimes(1);
    expect(navigateMock).toBeCalledWith("/");
  });

  it("no navigation when createPlayer returns a non-201 status code", async () => {
    const setIsLoggedIn = jest.fn();
    render(<PlayersCreate setIsLoggedIn={setIsLoggedIn}></PlayersCreate>);
    const nameInput = screen.getByLabelText("Name");
    const passwordInput = screen.getByLabelText("Password");
    const createButton = screen.getByText("Create");

    fireEvent.change(nameInput, { target: { value: "wronguser" } });
    fireEvent.change(passwordInput, { target: { value: "wrongpassword" } });
    await fireEvent.click(createButton);
    expect(createPlayer).toBeCalledTimes(1);
    expect(createPlayer).toBeCalledWith("wronguser", "wrongpassword");
    expect(setIsLoggedIn).not.toBeCalled();
    expect(navigateMock).not.toBeCalled();
  });
});
