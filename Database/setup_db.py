from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from werkzeug.security import generate_password_hash
from datetime import date

Base = declarative_base()

# --- Models ---
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    todos = relationship('Gym', back_populates='user')


class Gym(Base):
    __tablename__ = 'gym_function'  # Use snake_case for table names (no spaces)

    id = Column(Integer, primary_key=True)
    meal = Column(String, nullable=False)
    reps = Column(Boolean, default=False)
    exercise_weight = Column(Float, nullable=True)  # ✅ Weight lifted
    exercise_date = Column(Date, default=date.today)  # ✅ Date of exercise
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='todos')

    def mark_as_done(self):
        self.reps = True

# --- Setup database connection ---
engine = create_engine('sqlite:///FITZONE.db', echo=True)  # echo=True shows SQL commands
Session = sessionmaker(bind=engine)
session = Session()

# --- Create tables ---
Base.metadata.drop_all(engine)  # Wipe old schema (CAUTION: data loss)
Base.metadata.create_all(engine)

# --- Insert users ---
user1 = User(username='john_doe', password=generate_password_hash('password123'))
user2 = User(username='jane_doe', password=generate_password_hash('mypassword'))
user3 = User(username='admin',password=generate_password_hash('123'))
session.add_all([user1, user2,user3])
session.commit()

# --- Insert gym tasks ---
gym1 = Gym(
    meal='High protein chicken meal',
    reps=True,
    exercise_weight=60.0,
    exercise_date=date(2025, 6, 4),
    user_id=user1.id
)

gym2 = Gym(
    meal='Leg day - squats',
    reps=False,
    exercise_weight=100.0,
    exercise_date=date(2025, 6, 6),
    user_id=user2.id
)

session.add_all([gym1, gym2])
session.commit()

print("✅ Users and gym entries inserted successfully.")