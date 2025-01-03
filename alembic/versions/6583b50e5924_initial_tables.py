"""Initial tables

Revision ID: 6583b50e5924
Revises:
Create Date: 2024-05-24 17:30:52.520717

"""

from typing import Sequence, Union

# TODO: Fix type ignore by moving alembic/ directory?
from alembic import op  # type: ignore[attr-defined]
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "853345b1c2f1"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "countries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "directors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("lb_url", sa.String(), nullable=False),
        sa.Column("last_updated", sa.DateTime(), nullable=True),
        sa.Column("last_checked", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("lb_url"),
    )
    op.create_table(
        "films",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("year", sa.Integer(), nullable=True),
        sa.Column("rating", sa.Numeric(), nullable=True),
        sa.Column("runtime", sa.Integer(), nullable=True),
        sa.Column("jw_url", sa.String(), nullable=True),
        sa.Column("lb_url", sa.String(), nullable=False),
        sa.Column("trailer_url", sa.String(), nullable=True),
        sa.Column("last_updated", sa.DateTime(), nullable=True),
        sa.Column("last_checked", sa.DateTime(), nullable=True),
        sa.Column("last_offers_checked", sa.DateTime(), nullable=True),
        sa.Column("last_offers_updated", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("lb_url"),
    )
    op.create_table(
        "genres",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "offers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "director_film_association_table",
        sa.Column("film_id", sa.Integer(), nullable=False),
        sa.Column("director_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["director_id"],
            ["directors.id"],
        ),
        sa.ForeignKeyConstraint(
            ["film_id"],
            ["films.id"],
        ),
        sa.PrimaryKeyConstraint("film_id", "director_id"),
    )
    op.create_table(
        "film_country_association_table",
        sa.Column("film_id", sa.Integer(), nullable=False),
        sa.Column("country_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["country_id"],
            ["countries.id"],
        ),
        sa.ForeignKeyConstraint(
            ["film_id"],
            ["films.id"],
        ),
        sa.PrimaryKeyConstraint("film_id", "country_id"),
    )
    op.create_table(
        "film_genre_association_table",
        sa.Column("film_id", sa.Integer(), nullable=False),
        sa.Column("genre_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["film_id"],
            ["films.id"],
        ),
        sa.ForeignKeyConstraint(
            ["genre_id"],
            ["genres.id"],
        ),
        sa.PrimaryKeyConstraint("film_id", "genre_id"),
    )
    op.create_table(
        "film_offer_association_table",
        sa.Column("film_id", sa.Integer(), nullable=False),
        sa.Column("offer_id", sa.Integer(), nullable=False),
        sa.Column("url", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["film_id"],
            ["films.id"],
        ),
        sa.ForeignKeyConstraint(
            ["offer_id"],
            ["offers.id"],
        ),
        sa.PrimaryKeyConstraint("film_id", "offer_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("film_offer_association_table")
    op.drop_table("film_genre_association_table")
    op.drop_table("film_country_association_table")
    op.drop_table("director_film_association_table")
    op.drop_table("offers")
    op.drop_table("genres")
    op.drop_table("films")
    op.drop_table("directors")
    op.drop_table("countries")
    # ### end Alembic commands ###
