import { axiosInstance, getHeaders } from "./api";
import { Teams, Team } from "../../data/interfaces/teams";

export async function getTeams(gameId: number): Promise<Teams | undefined> {
  try {
    const config = getHeaders();
    const response = await axiosInstance.get(`/games/${gameId}/teams`, config);
    if (response.status === 200) {
      const teams = response.data as Teams;
      return teams;
    }
    return undefined;
  } catch (error) {
    return undefined;
  }
}

export async function createTeam(
  gameId: number,
  teamName: string
): Promise<Team | undefined> {
  try {
    const config = getHeaders();
    const response = await axiosInstance.post(
      `/games/${gameId}/teams`,
      { team_name: teamName },
      config
    );
    if (response.status === 200) {
      const team = response.data as Team;
      return team;
    }
    return undefined;
  } catch (error) {
    return undefined;
  }
}

export async function joinTeam(gameId: number, teamId: number) : Promise<Team | undefined> {
  try {
    const config = getHeaders();
    const response = await axiosInstance.post(
      `/games/${gameId}/teams/${teamId}`,
      { },
      config
    );
    if (response.status === 200) {
      const team = response.data as Team;
      return team;
    }
    return undefined;
  } catch (error) {
    return undefined;
  }
}
