from sqlalchemy import create_engine, MetaData, \
                       Table, Column, String, Date, insert
import config
import logging

engine = create_engine(config.DATABASE_URL, echo=True)
devops_news = None


def create_tables():
    global devops_news
    meta = MetaData()

    devops_news = Table(
        'devops_news', meta,
        Column('id', String(300), primary_key=True),
        Column('subject', String(200)),
        Column('tags', String(700)),
        Column('date', Date),
        Column('author', String(50)),
        Column('link', String(200)),
    )
    meta.create_all(engine)
    logging.info("Create the devops_news Table")


def insert_data(data_list):
    try:
        conn = engine.connect()
        stmt = insert(devops_news).values(
            [
                {
                 'id': id, 'subject': subject, 'tags': tags,
                 'date': date, 'author': author, 'link': link
                }
                for id, subject, tags, date, author, link in data_list
            ]
            )
        with engine.begin() as conn:
            conn.execute(stmt)

    except Exception as e:
        logging.error(e)
