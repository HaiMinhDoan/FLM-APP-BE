from app.model.model import Base, engine
Base.metadata.create_all(bind=engine)