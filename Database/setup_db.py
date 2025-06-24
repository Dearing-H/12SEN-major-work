from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import date

Base = declarative_base()

# --- Models ---
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    gym_tasks = relationship('Gym', back_populates='user')


class Gym(Base):
    __tablename__ = 'gym_function'  

    id = Column(Integer, primary_key=True)
    meal = Column(String, nullable=False)
    reps = Column(Boolean, default=False)
    calories = Column(Float, nullable=True)  
    protein = Column(Float, nullable=True)  
    carbs = Column(Float, nullable=True) 
    fats = Column(Float, nullable=True) 
    water = Column(Float, nullable=True)
    exercise_type = Column(String, nullable=False)  
    exercise_duration = Column(Float, nullable=True) 
    exercise_weight = Column(Float, nullable=True)  
    exercise_date = Column(Date, default=date.today)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='gym_tasks')

    def mark_as_done(self):
        self.reps = True

# --- Setup database connection ---
engine = create_engine('sqlite:///FITZONE.db', echo=True)  # echo=True shows SQL commands
Session = sessionmaker(bind=engine)
session = Session()

# --- Create tables ---
Base.metadata.drop_all(engine)  # Wipe old schema (CAUTION: data loss)
Base.metadata.create_all(engine)

