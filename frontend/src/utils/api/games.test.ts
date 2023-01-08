import * as api from "./api";
import { createGame, getGames } from "./games";

jest.mock("./api", () => {
  return {
    getHeaders: jest.fn().mockReturnValue({
      headers: {
        Authorization: `bearer abc`,
      },
    }),
    axiosInstance: {},
  };
});

describe("getGames", () => {
  it("should return a list of games on success", async () => {
    const mockResponse = {
      status: 200,
      data: [
        {
          gameId: 1,
          roundOneDone: true,
          roundTwoDone: false,
          roundThreeDone: false,
          owner: {
            playerId: 1,
            name: "John",
          },
        },
        {
          gameId: 2,
          roundOneDone: true,
          roundTwoDone: true,
          roundThreeDone: false,
          owner: {
            playerId: 2,
            name: "Jane",
          },
        },
      ],
    };
    api.axiosInstance.get = jest.fn().mockReturnValue(mockResponse);
    const games = await getGames();
    expect(api.getHeaders).toBeCalledTimes(1);
    expect(api.axiosInstance.get).toBeCalledTimes(1);
    expect(api.axiosInstance.get).toBeCalledWith("/games", {
      headers: { Authorization: `bearer abc` },
    });
    expect(games).toEqual(mockResponse.data);
  });

  it("should return undefined when the API call fails", async () => {
    api.axiosInstance.get = jest.fn().mockReturnValue({
      status: 400,
      data: { error: "invalid login credentials" },
    });
    const games = await getGames();
    expect(games).toEqual(undefined);
  });

  it("should return undefined when an unexpected error occurs", async () => {
    api.axiosInstance.get = jest.fn().mockImplementation(() => {
      throw new Error("unexpected error");
    });
    const games = await getGames();
    expect(games).toEqual(undefined);
  });
});

describe("createGame", () => {
  it('should return a game that is being made', async () => {
    const mockResponse = {
      status: 201,
      data: {
        gameId: 1,
        roundOneDone: false,
        roundTwoDone: false,
        roundThreeDone: false,
        owner: {
          playerId: 1,
          name: "John",
        },
      },
    };
    api.axiosInstance.post = jest.fn().mockReturnValue(mockResponse);
    const game = await createGame();
    expect(api.getHeaders).toBeCalledTimes(1);
    expect(api.axiosInstance.post).toBeCalledTimes(1);
    expect(api.axiosInstance.post).toBeCalledWith("/games", {},{
      headers: { Authorization: `bearer abc` },
    });
    expect(game).toEqual(mockResponse.data);
  });
  
  it("should return undefined when the API call fails", async () => {
    api.axiosInstance.post = jest.fn().mockReturnValue({
      status: 400,
      data: { error: "invalid login credentials" },
    });
    const games = await createGame();
    expect(api.getHeaders).toBeCalledTimes(1);
    expect(games).toEqual(undefined);
  });

  it("should return undefined when the API call fails", async () => {
    api.axiosInstance.post = jest.fn().mockImplementation(() => {
      throw new Error("unexpected error");
    });
    const games = await createGame();
    expect(api.getHeaders).toBeCalledTimes(1);
    expect(games).toEqual(undefined);
  });
});