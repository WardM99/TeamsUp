export interface Card {
  cardId: number;
  points: number;
  topic: string;
}

export interface Cards {
  cards: Card[];
}
