import { render, fireEvent, screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import PlayersLogin from "./PlayersLogin";
import { login } from "../../utils/api/player";

const navigateMock = jest.fn();

jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useNavigate: () => navigateMock,
}));

jest.mock("../../utils/api/player", () => {
  return {
    login: jest.fn().mockImplementation((name: string, password: string) => {
      if (name === "testuser" && password === "testpassword") return 200;
      return 400;
    }),
  };
});

describe("PlayersLogin", () => {
  /*
  it("there is a nameInput, passwordInput, loginButton and registerButton", async () => {
    render(<PlayersLogin></PlayersLogin>);
    const nameInput = screen.getByLabelText("Name");
    const passwordInput = screen.getByLabelText("Password");
    const loginButton = screen.getByText("Login");
    const registerButton = screen.getByText("Register");

    expect(nameInput).toBeInTheDocument();
    expect(passwordInput).toBeInTheDocument();
    expect(loginButton).toBeInTheDocument();
    expect(registerButton).toBeInTheDocument();
  });

  it("form submission calls login function with correct arguments", async () => {
    render(<PlayersLogin></PlayersLogin>);
    const nameInput = screen.getByLabelText("Name");
    const passwordInput = screen.getByLabelText("Password");
    const loginButton = screen.getByText("Login");

    fireEvent.change(nameInput, { target: { value: "testuser" } });
    fireEvent.change(passwordInput, { target: { value: "testpassword" } });
    await fireEvent.click(loginButton);

    expect(login).toBeCalledTimes(1);
    expect(navigateMock).toBeCalledTimes(1);
    expect(navigateMock).toBeCalledWith("/");
  });

  it("no navigation when password is wrong", async () => {
    render(<PlayersLogin></PlayersLogin>);
    const nameInput = screen.getByLabelText("Name");
    const passwordInput = screen.getByLabelText("Password");
    const loginButton = screen.getByText("Login");

    fireEvent.change(nameInput, { target: { value: "testuser" } });
    fireEvent.change(passwordInput, { target: { value: "testpassword123" } });
    await fireEvent.click(loginButton);

    expect(login).toBeCalledTimes(1);
    expect(navigateMock).toBeCalledTimes(0);
  });

  it("no navigation when name is wrong", async () => {
    render(<PlayersLogin></PlayersLogin>);
    const nameInput = screen.getByLabelText("Name");
    const passwordInput = screen.getByLabelText("Password");
    const loginButton = screen.getByText("Login");

    fireEvent.change(nameInput, { target: { value: "testuse" } });
    fireEvent.change(passwordInput, { target: { value: "testpassword" } });
    await fireEvent.click(loginButton);

    expect(login).toBeCalledTimes(1);
    expect(navigateMock).toBeCalledTimes(0);
  });

  it("no createPlayer when name is not filled in", async () => {
    render(<PlayersLogin></PlayersLogin>);
    const passwordInput = screen.getByLabelText("Password");
    const loginButton = screen.getByText("Login");

    fireEvent.change(passwordInput, { target: { value: "testpassword" } });
    await fireEvent.click(loginButton);

    expect(login).toBeCalledTimes(0);
  });

  it("no createPlayer when password is not filled in", async () => {
    render(<PlayersLogin></PlayersLogin>);
    const nameInput = screen.getByLabelText("Name");
    const loginButton = screen.getByText("Login");

    fireEvent.change(nameInput, { target: { value: "user" } });
    await fireEvent.click(loginButton);

    expect(login).toBeCalledTimes(0);
  });

  it("register button navigates to /register", async () => {
    render(<PlayersLogin></PlayersLogin>);
    const registerButton = screen.getByText("Register");
    expect(registerButton.getAttribute("href")).toEqual("/register");
  });
  */
});
