from pytest_bdd import parsers, when, then
from sqlalchemy import insert, select
from sqlalchemy.sql.schema import MetaData, Table, Column
from sqlalchemy.sql.sqltypes import Integer, String


@when('Movies table is created', target_fixture='movies_table')
def movies_table_is_created(database_engine):
    """Create Movies table"""
    metadata_obj = MetaData()
    movies_table = Table('Movies', metadata_obj,
        Column('Title', String(10), primary_key=True, nullable=False),
        Column('Director', String(15)),
        Column('Year', Integer)
    )
    metadata_obj.create_all(database_engine)
    return movies_table

@when(
    parsers.parse('{movie_name} directed by {director} is published on {year:d} is added')
)
def directed_by_is_published_on(database_engine, movies_table, movie_name, director, year):
    """Insert data into movies table"""
    insert_stmt = insert(movies_table).values(
        Title=movie_name, Director=director, Year=year
    ).compile()
    with database_engine.begin() as conn:
        conn.execute(insert_stmt)

@then('movie should be persisted in the DB')
def movie_should_be_persisted_in_the_DB(database_engine, movies_table, movie_name):
    select_stmt = select(movies_table).where(movies_table.c.Title == movie_name)
    with database_engine.connect() as conn:
        result = conn.execute(select_stmt).all()
        assert len(result) == 1, 'Only one record should be added'
        assert result[0][0] == movie_name, 'Movie with specified title should be fetched'
