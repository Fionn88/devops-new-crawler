import pytest
from sqlalchemy import inspect, text
import datetime

from src.database import create_tables, insert_data, engine


@pytest.fixture(scope='module')
def setup_database():
    create_tables()
    yield
    engine.dispose()


def test_create_table(setup_database):
    inspector = inspect(engine)
    assert 'devops_news' in inspector.get_table_names()


def test_insert_data(setup_database):
    test_data = [
        ['1', 'subject1', 'tag1,tag2',
         datetime.date.today(), 'author1', 'link1'],
        ['2', 'subject2', 'tag3,tag4',
         datetime.date.today() + datetime.timedelta(days=1),
         'author2', 'link2']
    ]
    insert_data(test_data)

    with engine.connect() as conn:
        result = conn.execute(text('SELECT * FROM devops_news')).fetchall()
        assert len(result) == 2
        assert result[0][1] == 'subject1'
        assert result[1][1] == 'subject2'
