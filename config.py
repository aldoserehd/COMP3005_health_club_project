from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_USER = "postgres"         
DB_PASS = "root"     
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "health_club"

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
