from models import Base
from sqlalchemy import create_engine
import os

# Get the absolute path to the directory where this file is located
basedir = os.path.abspath(os.path.dirname(__file__))
# Create the full path for the database file
db_path = os.path.join(basedir, "FITZONE.db")
engine = create_engine(f"sqlite:///{db_path}")

Base.metadata.drop_all(engine)   # ⚠️ Destroys data!
Base.metadata.create_all(engine)

print("Database reset.")

if __name__ == '__main__':
    # Database setup
    # This part is redundant now but harmless.
    # The main script logic already creates the db.
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)
    print("Database and tables created successfully.")