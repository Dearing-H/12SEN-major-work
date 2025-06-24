from sqlalchemy import Column, Integer, String, Boolean, Float, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import date, datetime, timezone

Base = declarative_base()

# Make sure to create tables before using the models
# Example usage (put this in your main app or a setup script, not in models.py):
# from sqlalchemy import create_engine
# engine = create_engine('sqlite:///your_database.db')
# Base.metadata.create_all(engine)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    # User stats
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    bmi = Column(Float, nullable=True)
    age = Column(Integer, nullable=True)
    activity_level = Column(Float, nullable=True)
    tdee = Column(Integer, nullable=True)
    last_exercise_name = Column(String, nullable=True)
    last_reps = Column(Integer, nullable=True)
    last_sets = Column(Integer, nullable=True)
    last_meal_description = Column(Text, nullable=True)
    current_weight = Column(Float, nullable=True)
    goal_weight = Column(Float, nullable=True)
    last_water_cups = Column(Integer, nullable=True)

    # Relationships
    gym_tasks = relationship('Gym', back_populates='user')
    bmi_records = relationship('BMIR', back_populates='user')
    calorie_records = relationship('CalorieRecord', back_populates='user')
    exercise_logs = relationship('ExerciseLog', back_populates='user')
    meal_logs = relationship('MealLog', back_populates='user')
    water_intakes = relationship('WaterIntake', back_populates='user')
    weight_goals = relationship('WeightGoal', back_populates='user')

    @classmethod
    def get_by_username(cls, session, username):
        return session.query(cls).filter_by(username=username).first()


class Gym(Base):
    __tablename__ = 'gym_function'

    id = Column(Integer, primary_key=True)
    meal = Column(String, nullable=False)
    reps = Column(Boolean, default=False)
    calories = Column(Float)
    protein = Column(Float)
    carbs = Column(Float)
    fats = Column(Float)
    water = Column(Float)
    exercise_type = Column(String, nullable=False)
    exercise_duration = Column(Float)
    exercise_weight = Column(Float)
    exercise_date = Column(Date, default=date.today)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='gym_tasks')

    def mark_as_done(self):
        self.reps = True


class BMIR(Base):
    __tablename__ = 'bmi_records'

    id = Column(Integer, primary_key=True)
    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    bmi = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='bmi_records')


class CalorieRecord(Base):
    __tablename__ = 'calorie_records'

    id = Column(Integer, primary_key=True)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    activity_level = Column(Float, nullable=False)
    tdee = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='calorie_records')


class ExerciseLog(Base):
    __tablename__ = 'exercise_logs'

    id = Column(Integer, primary_key=True)
    exercise_name = Column(String(100), nullable=False)
    reps = Column(Integer, nullable=False)
    sets = Column(Integer, nullable=False)
    total_reps = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='exercise_logs')


class MealLog(Base):
    __tablename__ = 'meal_logs'

    id = Column(Integer, primary_key=True)
    meal_description = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='meal_logs')


class WeightGoal(Base):
    __tablename__ = 'weight_goals'

    id = Column(Integer, primary_key=True)
    current_weight = Column(Float, nullable=False)
    goal_weight = Column(Float, nullable=False)
    difference = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='weight_goals')


class WaterIntake(Base):
    __tablename__ = 'water_intake'

    id = Column(Integer, primary_key=True)
    cups = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='water_intakes')


