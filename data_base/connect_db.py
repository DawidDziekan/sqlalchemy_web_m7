from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://postgres:asdf@localhost:5432/postgres")
Session = sessionmaker(bind=engine)
session = Session()