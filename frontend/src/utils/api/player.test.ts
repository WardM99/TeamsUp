import * as api from './api';
import * as auth from '../local-storage.ts/auth'
import { createPlayer, login, logout, currentPlayer } from "./player";

jest.mock('./api', () => {
  return {
    getHeaders: jest.fn().mockReturnValue({
      headers: {
          "Authorization": `bearer abc`
      }
    }),
    axiosInstance: { }
  }
});

jest.mock('../local-storage.ts/auth', () => {
  return {
    setAccessToken: jest.fn(),
    setTokenType: jest.fn(),
  }
})

describe("createPlayer", () => {

    
  it("should return 201 with valid input", async () => {
    
    const response = {
      status: 201,
      data: {
        access_token: "test_access_token",
        token_type: "test_token_type",
        user: { name: "testuser" },
      },
    };
    
    api.axiosInstance.post = jest.fn().mockReturnValue(response);

    const name = "testuser";
    const password = "testpass";
    const status = await createPlayer(name, password);
    expect(auth.setAccessToken).toBeCalledTimes(1);
    expect(auth.setAccessToken).toHaveBeenCalledWith("test_access_token");
    expect(auth.setTokenType).toBeCalledTimes(1);
    expect(auth.setTokenType).toHaveBeenCalledWith("test_token_type");
    expect(status).toEqual(201);
  });
  
  it("should return 400 with empty name", async () => {
    const response: any = {
      status: 400,
      data: {
        error: "Invalid name",
      },
    };
    api.axiosInstance.post = jest.fn().mockReturnValue(response);

    const name = "";
    const password = "testpass";
    const status = await createPlayer(name, password);
    expect(status).toBe(400);
  });

  it("should return 400 with empty password", async () => {
    const response: any = {
      status: 400,
      data: {
        error: "Invalid password",
      },
    };
    api.axiosInstance.post = jest.fn().mockReturnValue(response);

    const name = "testuser";
    const password = "";
    const status = await createPlayer(name, password);
    expect(status).toBe(400);
  })

  test("should return a status code of 500 when an unexpected error occurs", async () => {
    api.axiosInstance.post = jest.fn().mockImplementation(() => {
      throw new Error("unexpected error");
    });

    const result = await createPlayer("test player", "password");
    expect(result).toBe(500);
  });
});

describe("login", () => {

  test("should return the correct status code when the login is successful", async () => {
    api.axiosInstance.post = jest.fn().mockReturnValue({
      status: 200,
      data: {
        access_token: "abc123",
        token_type: "bearer",
        user: { id: 1, name: "test player" },
      },
    });

    const result = await login("test player", "password");
    expect(result).toBe(200);
    expect(auth.setAccessToken).toBeCalledTimes(1);
    expect(auth.setAccessToken).toHaveBeenCalledWith("abc123");
    expect(auth.setTokenType).toBeCalledTimes(1);
    expect(auth.setTokenType).toHaveBeenCalledWith("bearer");
  });

  test("should return the correct status code when the login fails", async () => {
    api.axiosInstance.post = jest.fn().mockReturnValue({
      status: 400,
      data: { error: "invalid login credentials" },
    });

    const result = await login("test player", "password");
    expect(result).toBe(400);
  });

  test("should return a status code of 500 when an unexpected error occurs", async () => {
    api.axiosInstance.post= jest.fn().mockImplementation(() => {
      throw new Error("unexpected error");
    });

    const result = await login("test player", "password");
    expect(result).toBe(500);
  });
});

describe('getUsers', () => {

  test('should make a GET request to the correct URL', async () => {
    api.axiosInstance.get = jest.fn()
    await currentPlayer();
    expect(api.getHeaders).toBeCalledTimes(1);
    expect(api.axiosInstance.get).toHaveBeenCalledWith('/players/current', {
      headers: {
          "Authorization": `bearer abc`
      }
    });
  });

  test('should return the current player when the API call is successful', async () => {
    api.axiosInstance.get = jest.fn().mockReturnValue({
      data: {
        playerId: 1,
        name: 'John'
      }
    });
    const player = await currentPlayer();
    expect(player).toEqual({
      playerId: 1,
      name: 'John'
    });
  });

  test('should return undefined when the API call fails', async () => {
    api.axiosInstance.get = jest.fn().mockRejectedValueOnce(new Error('API call failled'));
    const player = await currentPlayer();
    expect(player).toBeUndefined();
  });
});

describe('logout', () => {
  test('should use setAccessToken and setTokenType once', () => {
    logout();
    expect(auth.setAccessToken).toBeCalledTimes(1);
    expect(auth.setAccessToken).toHaveBeenCalledWith(null);
    expect(auth.setTokenType).toBeCalledTimes(1);
    expect(auth.setTokenType).toHaveBeenCalledWith(null);
  })
});
