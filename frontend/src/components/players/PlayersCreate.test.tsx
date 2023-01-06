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
    render(<PlayersCreate></PlayersCreate>);
    const nameInput = screen.getByLabelText("Name");
    const passwordInput = screen.getByLabelText("Password");
    const loginButton = screen.getByText("Login");
    const createButton = screen.getByText("Create");

    expect(nameInput).toBeInTheDocument();
    expect(passwordInput).toBeInTheDocument();
    expect(loginButton).toBeInTheDocument();
    expect(createButton).toBeInTheDocument();
  });

  it("form submission calls login function with correct arguments", async () => {
    render(<PlayersCreate></PlayersCreate>);
    const nameInput = screen.getByLabelText("Name");
    const passwordInput = screen.getByLabelText("Password");
    const createButton = screen.getByText("Create");

    fireEvent.change(nameInput, { target: { value: "testuser" } });
    fireEvent.change(passwordInput, { target: { value: "testpassword" } });
    await fireEvent.click(createButton);

    expect(createPlayer).toBeCalledTimes(1);
    expect(navigateMock).toBeCalledTimes(1);
    expect(navigateMock).toBeCalledWith("/");
  });

  it("no navigation when password is wrong", async () => {
    render(<PlayersCreate></PlayersCreate>);
    const nameInput = screen.getByLabelText("Name");
    const passwordInput = screen.getByLabelText("Password");
    const createButton = screen.getByText("Create");

    fireEvent.change(nameInput, { target: { value: "testuser" } });
    fireEvent.change(passwordInput, { target: { value: "empty" } });
    await fireEvent.click(createButton);

    expect(createPlayer).toBeCalledTimes(1);
    expect(navigateMock).toBeCalledTimes(0);
  });

  it("no navigation when name is wrong", async () => {
    render(<PlayersCreate></PlayersCreate>);
    const nameInput = screen.getByLabelText("Name");
    const passwordInput = screen.getByLabelText("Password");
    const createButton = screen.getByText("Create");

    fireEvent.change(nameInput, { target: { value: "empty" } });
    fireEvent.change(passwordInput, { target: { value: "testpassword" } });
    await fireEvent.click(createButton);

    expect(createPlayer).toBeCalledTimes(1);
    expect(navigateMock).toBeCalledTimes(0);
  });

  it("no createPlayer when name is not filled in", async () => {
    render(<PlayersCreate></PlayersCreate>);
    const passwordInput = screen.getByLabelText("Password");
    const createButton = screen.getByText("Create");

    fireEvent.change(passwordInput, { target: { value: "testpassword" } });
    await fireEvent.click(createButton);

    expect(createPlayer).toBeCalledTimes(0);
  });

  it("no createPlayer when password is not filled in", async () => {
    render(<PlayersCreate></PlayersCreate>);
    const nameInput = screen.getByLabelText("Name");
    const createButton = screen.getByText("Create");

    fireEvent.change(nameInput, { target: { value: "user" } });
    await fireEvent.click(createButton);

    expect(createPlayer).toBeCalledTimes(0);
  });

  it("register button navigates to /register", async () => {
    render(<PlayersCreate></PlayersCreate>);
    const loginButton = screen.getByText("Login");
    expect(loginButton.getAttribute("href")).toEqual("/login");
  });
});
