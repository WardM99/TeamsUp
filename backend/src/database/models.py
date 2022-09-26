"""Here are all the database models"""
# pylint: disable=too-few-public-methods
from __future__ import annotations

from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Player(Base):
    """The data of a player"""
    __tablename__ = "players"

    player_id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.team_id"))
    name: str = Column(Text, nullable=False, unique=True)
    password: str = Column(Text, nullable=False)

    teams: list[Team] = relationship(
                            "Team",
                            secondary="player_teams",
                            back_populates="players",
                            uselist=False,
                            lazy="selectin"
                        )



class Team(Base):
    """The data of teams"""
    __tablename__ = "teams"

    team_id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.game_id"))
    team_name: str = Column(Text, nullable=False, unique=False)

    players: list[Player] = \
        relationship("Player", secondary="player_teams", back_populates="teams")

    game: Game = relationship("Game", back_populates="teams", uselist=False, lazy="selectin")

class Game(Base):
    """The data of a game that has been played or is playing"""
    __tablename__ = "games"

    game_id = Column(Integer, primary_key=True, index=True)
    round_one_done: bool = Column(Boolean, nullable=False, default=False)
    round_two_done: bool = Column(Boolean, nullable=False, default=False)
    round_three_done: bool = Column(Boolean, nullable=False, default=False)

    teams: list[Team] =  \
        relationship("Team", back_populates="game", cascade="all, delete-orphan")


player_teams = Table(
    "player_teams", Base.metadata,
    Column("player_id", ForeignKey("players.player_id")),
    Column("team_id", ForeignKey("teams.team_id"))
)
