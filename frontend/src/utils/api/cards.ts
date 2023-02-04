import { axiosInstance, getHeaders } from "./api";
import { Cards } from "../../data/interfaces/cards";

export async function getCards(): Promise<Cards | undefined> {
  try {
    const config = getHeaders();
    const response = await axiosInstance.get(`/cards`, config);
    if (response.status === 200) {
      const cards = response.data as Cards;
      return cards;
    }
    return undefined;
  } catch (error) {
    return undefined;
  }
}

export async function addCardToGame(
  gameId: number,
  cardId: number
): Promise<number> {
  try {
    const config = getHeaders();
    const response = await axiosInstance.post(
      `/games/${gameId}/cards`,
      { card_id: cardId },
      config
    );
    return response.status;
  } catch (error) {
    return 500;
  }
}
