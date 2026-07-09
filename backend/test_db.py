from sqlalchemy import text

from app.database.session import engine


with engine.connect() as connection:
    result = connection.execute(text("SELECT version();"))

    print(result.scalar())