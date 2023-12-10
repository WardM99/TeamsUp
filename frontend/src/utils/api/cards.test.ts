import * as api from "./api";
import { Cards, Card } from "../../data/interfaces/cards";
import { addCardToGame, getCards } from "./cards";

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

describe("getCards", () => {
  it("should return a list of cards on success", async () => {
    const card1: Card = {
      cardId: 1,
      points: 10,
      topic: "History",
    };
    const card2: Card = {
      cardId: 2,
      points: 5,
      topic: "Geography",
    };
    const card3: Card = {
      cardId: 3,
      points: 15,
      topic: "Science",
    };
    const card4: Card = {
      cardId: 4,
      points: 20,
      topic: "Mathematics",
    };
    const cards: Cards = {
      cards: [card1, card2, card3, card4],
    };
    const mockResponse = {
      status: 200,
      data: cards,
    };
    api.axiosInstance.get = jest.fn().mockReturnValue(mockResponse);
    const response = await getCards();
    expect(api.getHeaders).toBeCalledTimes(1);
    expect(api.axiosInstance.get).toBeCalledTimes(1);
    expect(api.axiosInstance.get).toBeCalledWith("/cards", {
      headers: { Authorization: `bearer abc` },
    });
    expect(response).toEqual(mockResponse.data);
  });
  it("should return undefined when the API call fails", async () => {
    api.axiosInstance.get = jest.fn().mockReturnValue({
      status: 400,
      data: { error: "invalid login credentials" },
    });
    const response = await getCards();
    expect(response).toEqual(undefined);
  });

  it("should return undefined when an unexpected error occurs", async () => {
    api.axiosInstance.get = jest.fn().mockImplementation(() => {
      throw new Error("unexpected error");
    });
    const response = await getCards();
    expect(response).toEqual(undefined);
  });
});

describe("addCardToGame", () => {
  it("should return 204 when everything goes well", async () => {
    api.axiosInstance.post = jest.fn().mockReturnValue({
      status: 204,
    });
    const response = await addCardToGame(1, 1);
    expect(api.getHeaders).toBeCalledTimes(1);
    expect(api.axiosInstance.post).toBeCalledTimes(1);
    expect(api.axiosInstance.post).toBeCalledWith(
      "/games/1/cards",
      {
        card_id: 1,
      },
      {
        headers: { Authorization: `bearer abc` },
      },
    );
    expect(response).toEqual(204);
  });

  it("should return 400 when the API call fails", async () => {
    api.axiosInstance.post = jest.fn().mockReturnValue({
      status: 400,
    });
    const response = await addCardToGame(1, 1);
    expect(response).toEqual(400);
  });

  it("should return 500 when an unexpected error occurs", async () => {
    api.axiosInstance.post = jest.fn().mockImplementation(() => {
      throw new Error("unexpected error");
    });
    const response = await addCardToGame(1, 1);
    expect(response).toEqual(500);
  });
});
