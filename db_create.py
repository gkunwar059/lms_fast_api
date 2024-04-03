from models import UserBook,User,Book,Base,Magazine,UserMagazine,Publisher,Category,Record,Role,Permission


from database.db_connection import engine
Base.metadata.create_all(engine)
