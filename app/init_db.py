from config import engine
from models.base import Base
from models import entities  # importing models so SQLAlchemy knows about them when creating tables


def init_db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")


if __name__ == "__main__":
    init_db()
