import * as api from "./api";
import { getTeams } from "./teams";
import { Teams, Team } from '../../data/interfaces/teams';


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
        const team1: Team = {
            teamId: 1,
            gameId: 1,
            teamName: 'Red Team',
            players: [
                {
                    playerId: 1,
                    name: 'Alice',
                },
                {
                    playerId: 2,
                    name: 'Bob',
                },
            ],
        };
        
        const team2: Team = {
            teamId: 2,
            gameId: 1,
            teamName: 'Blue Team',
            players: [
                {
                    playerId: 3,
                    name: 'Eve',
                },
                {
                    playerId: 4,
                    name: 'Dave',
                },
            ],
        };
        
        const teams: Teams = {
            teams: [team1, team2],
        };


      const mockResponse = {
        status: 200,
        data: teams,
      };
      api.axiosInstance.get = jest.fn().mockReturnValue(mockResponse);
      const games = await getTeams(1);
      expect(api.getHeaders).toBeCalledTimes(1);
      expect(api.axiosInstance.get).toBeCalledTimes(1);
      expect(api.axiosInstance.get).toBeCalledWith("/games/1/teams", {
        headers: { Authorization: `bearer abc` },
      });
      expect(games).toEqual(mockResponse.data);
    });
  
    it("should return undefined when the API call fails", async () => {
      api.axiosInstance.get = jest.fn().mockReturnValue({
        status: 400,
        data: { error: "invalid login credentials" },
      });
      const games = await getTeams(1);
      expect(games).toEqual(undefined);
    });
  
    it("should return undefined when an unexpected error occurs", async () => {
      api.axiosInstance.get = jest.fn().mockImplementation(() => {
        throw new Error("unexpected error");
      });
      const games = await getTeams(1);
      expect(games).toEqual(undefined);
    });
  });