from app.model.model import Base, engine, get_db, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT
import psycopg2
Base.metadata.create_all(bind=engine)
