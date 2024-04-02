from sqlalchemy import create_engine,engine
from sqlalchemy.orm import Session,sessionmaker
from decouple import config

DATABASE_CONNECTION = config("database_connection")

try:
    engine = create_engine(DATABASE_CONNECTION, echo=False)
    engine.connect()
    print("Connection Okay")

except Exception as er:
    print(er)
    print("connection is not successful ")


with Session(engine) as session:
    Session = sessionmaker(bind=engine)
    session = Session()

# from models import (
#     UserBook,
#     User,
#     Book,
#     Base,
#     engine,
#     Magazine,
#     UserMagazine,
#     Publisher,
#     Category,
#     Record,
#     Role,
# )


# Base.metadata.create_all(engine)
