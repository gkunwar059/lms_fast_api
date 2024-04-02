from database.db_connection import engine
from models import (
    UserBook,
    User,
    Book,
    Base,
    Magazine,
    UserMagazine,
    Publisher,
    Category,
    Record,
    Role,
)

Base.metadata.create_all(engine)
