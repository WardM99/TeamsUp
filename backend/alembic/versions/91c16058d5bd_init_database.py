"""init database

Revision ID: 91c16058d5bd
Revises: 
Create Date: 2022-09-27 19:24:11.441292

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91c16058d5bd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cards',
    sa.Column('card_id', sa.Integer(), nullable=False),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.Column('topic', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('card_id')
    )
    with op.batch_alter_table('cards', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_cards_card_id'), ['card_id'], unique=False)

    op.create_table('games',
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('may_suggests_cards', sa.Boolean(), nullable=False),
    sa.Column('game_started', sa.Boolean(), nullable=False),
    sa.Column('round_one_done', sa.Boolean(), nullable=False),
    sa.Column('round_two_done', sa.Boolean(), nullable=False),
    sa.Column('round_three_done', sa.Boolean(), nullable=False),
    sa.Column('next_team_index', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['players.player_id'], ),
    sa.PrimaryKeyConstraint('game_id')
    )
    with op.batch_alter_table('games', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_games_game_id'), ['game_id'], unique=False)

    op.create_table('players',
    sa.Column('player_id', sa.Integer(), nullable=False),
    sa.Column('current_team_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['current_team_id'], ['teams.team_id'], ),
    sa.PrimaryKeyConstraint('player_id'),
    sa.UniqueConstraint('name')
    )
    with op.batch_alter_table('players', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_players_player_id'), ['player_id'], unique=False)

    op.create_table('teams',
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.Column('team_name', sa.Text(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('next_player_index', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['games.game_id'], ),
    sa.PrimaryKeyConstraint('team_id')
    )
    with op.batch_alter_table('teams', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_teams_team_id'), ['team_id'], unique=False)

    op.create_table('card_games',
    sa.Column('card_id', sa.Integer(), nullable=True),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.Column('guessed', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['card_id'], ['cards.card_id'], ),
    sa.ForeignKeyConstraint(['game_id'], ['games.game_id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('card_games')
    with op.batch_alter_table('teams', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_teams_team_id'))

    op.drop_table('teams')
    with op.batch_alter_table('players', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_players_player_id'))

    op.drop_table('players')
    with op.batch_alter_table('games', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_games_game_id'))

    op.drop_table('games')
    with op.batch_alter_table('cards', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_cards_card_id'))

    op.drop_table('cards')
    # ### end Alembic commands ###
