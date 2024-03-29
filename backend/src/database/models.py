"""Here are all the database models"""
# pylint: disable=too-few-public-methods
from __future__ import annotations

from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text, Table
from sqlalchemy.orm import declarative_base, relationship, Mapped

Base = declarative_base()

class Player(Base):
    """The data of a player"""
    __tablename__ = "players"

    player_id = Column(Integer, primary_key=True, index=True)
    current_team_id = Column(Integer, ForeignKey("teams.team_id"))
    name: str = Column(Text, nullable=False, unique=True)
    password: str = Column(Text, nullable=False)

    current_team: Mapped[Team] = relationship(
        "Team",
        back_populates="players",
        uselist=False,
        lazy="selectin"
    )
    owned_games: Mapped[list[Game]] = relationship(
        "Game",
        back_populates="owner",
        cascade="all, delete-orphan"
    )



class Team(Base):
    """The data of teams"""
    __tablename__ = "teams"

    team_id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.game_id"))
    team_name: str = Column(Text, nullable=False, unique=False)
    score = Column(Integer, default=0)

    next_player_index: int = Column(Integer, default=0)

    game: Mapped[Game] = relationship(
        "Game", back_populates="teams", uselist=False, lazy="selectin"
    )
    players: Mapped[list[Player]] = relationship(
        "Player",
        back_populates="current_team",
        cascade="all, delete-orphan"
    )


class Game(Base):
    """The data of a game that has been played or is playing"""
    __tablename__ = "games"

    game_id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("players.player_id"))
    game_started: bool = Column(Boolean, nullable=False, default=False)
    may_suggests_cards: bool = Column(Boolean, nullable=False, default=False)
    round_one_done: bool = Column(Boolean, nullable=False, default=False)
    round_two_done: bool = Column(Boolean, nullable=False, default=False)
    round_three_done: bool = Column(Boolean, nullable=False, default=False)

    next_team_index: int = Column(Integer, default=0)

    teams: Mapped[list[Team]] = relationship(
        "Team", back_populates="game", cascade="all, delete-orphan"
    )

    cards: Mapped[list[Card]] = relationship(
        "Card", secondary="card_games", back_populates="games"
    )
    owner: Mapped[Player] = relationship(
        "Player",
        back_populates="owned_games",
        uselist=False,
        lazy="selectin"
    )


class Card(Base):
    """The data of a card"""
    __tablename__ = "cards"

    card_id = Column(Integer, primary_key=True, index=True)
    points: int = Column(Integer, nullable=False)
    topic: str = Column(Text, nullable=False)

    games: Mapped[list[Game]] = relationship("Game", secondary="card_games", back_populates="cards")


card_games = Table(
    "card_games", Base.metadata,
    Column("card_id", ForeignKey("cards.card_id")),
    Column("game_id", ForeignKey("games.game_id")),
    Column("guessed", Boolean(), default=False)
)
