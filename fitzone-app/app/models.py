from sqlalchemy import Column, Integer, String, Boolean, Float, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import date, datetime, timezone

Base = declarative_base()

# Base class for all ORM models.
# Ensure to create tables before using the models.
# Example usage (put this in your main app or a setup script, not in models.py):
# from sqlalchemy import create_engine
# engine = create_engine('sqlite:///your_database.db')
# Base.metadata.create_all(engine)

class User(Base):
    """
    Represents a user of the FitZone application.
    Stores authentication credentials and personal stats.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)  # Unique username for login
    password = Column(String, nullable=False)  # Hashed password for authentication

    # User physical stats and metrics
    weight = Column(Float, nullable=True)  # User's weight in kilograms
    height = Column(Float, nullable=True)  # User's height in centimeters
    bmi = Column(Float, nullable=True)  # Body Mass Index calculated for user
    age = Column(Integer, nullable=True)  # User's age in years
    activity_level = Column(Float, nullable=True)  # Activity multiplier for TDEE calculation
    tdee = Column(Integer, nullable=True)  # Total Daily Energy Expenditure estimate
    current_weight = Column(Float, nullable=True)  # Current recorded weight
    goal_weight = Column(Float, nullable=True)  # Target weight user aims to achieve

    # Relationships to related records
    gym_tasks = relationship('Gym', back_populates='user')  # Gym workout records
    bmi_records = relationship('BMIR', back_populates='user')  # Historical BMI records
    calorie_records = relationship('CalorieRecord', back_populates='user')  # Calorie tracking logs
    exercise_logs = relationship('ExerciseLog', back_populates='user')  # Exercise session logs
    meal_logs = relationship('MealLog', back_populates='user')  # Meal intake logs
    water_intakes = relationship('WaterIntake', back_populates='user')  # Water consumption logs
    weight_goals = relationship('WeightGoal', back_populates='user')  # Weight goal tracking
    login_sessions = relationship('LoginSession', back_populates='user')  # User login session records

    @classmethod
    def get_by_username(cls, session, username):
        """
        Retrieve a user by their username.
        """
        return session.query(cls).filter_by(username=username).first()


class Gym(Base):
    """
    Represents a gym activity or workout entry for a user.
    Includes details about exercises, nutrition, and hydration.
    """
    __tablename__ = 'gym_function'

    id = Column(Integer, primary_key=True)
    meal = Column(String, nullable=False)  # Description of meal consumed
    reps = Column(Boolean, default=False)  # Indicates if reps were completed for the exercise
    calories = Column(Float)  # Calories burned or consumed
    protein = Column(Float)  # Protein intake in grams
    carbs = Column(Float)  # Carbohydrate intake in grams
    fats = Column(Float)  # Fat intake in grams
    water = Column(Float)  # Water intake in liters
    exercise_type = Column(String, nullable=False)  # Type of exercise performed
    exercise_duration = Column(Float)  # Duration in minutes
    exercise_weight = Column(Float)  # Weight used during exercise in kilograms
    exercise_date = Column(Date, default=date.today)  # Date of the exercise session

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Owner user reference
    user = relationship('User', back_populates='gym_tasks')

    def mark_as_done(self):
        """
        Mark the exercise as completed by setting reps to True.
        """
        self.reps = True


class BMIR(Base):
    """
    Stores historical BMI records for users.
    """
    __tablename__ = 'bmi_records'

    id = Column(Integer, primary_key=True)
    weight = Column(Float, nullable=False)  # Weight at the time of record
    height = Column(Float, nullable=False)  # Height at the time of record
    bmi = Column(Float, nullable=False)  # Calculated BMI value
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # Record timestamp
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Associated user

    user = relationship('User', back_populates='bmi_records')


class CalorieRecord(Base):
    """
    Tracks calorie-related data and TDEE calculations for users.
    """
    __tablename__ = 'calorie_records'

    id = Column(Integer, primary_key=True)
    age = Column(Integer, nullable=False)  # User age at record time
    weight = Column(Float, nullable=False)  # Weight at record time
    height = Column(Float, nullable=False)  # Height at record time
    activity_level = Column(Float, nullable=False)  # Activity factor used
    tdee = Column(Integer, nullable=False)  # Calculated Total Daily Energy Expenditure
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # Record timestamp
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Associated user

    user = relationship('User', back_populates='calorie_records')


class ExerciseLog(Base):
    """
    Logs details of individual exercise sessions.
    """
    __tablename__ = 'exercise_logs'

    id = Column(Integer, primary_key=True)
    exercise_name = Column(String(100), nullable=False)  # Name of the exercise performed
    reps = Column(Integer, nullable=False)  # Number of repetitions per set
    sets = Column(Integer, nullable=False)  # Number of sets performed
    total_reps = Column(Integer, nullable=False)  # Total repetitions (reps * sets)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # Time of log entry
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Associated user

    user = relationship('User', back_populates='exercise_logs')


class MealLog(Base):
    """
    Records meal descriptions and timestamps for users.
    """
    __tablename__ = 'meal_logs'

    id = Column(Integer, primary_key=True)
    meal_description = Column(Text, nullable=False)  # Description of the meal consumed
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # Time of meal
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Associated user

    user = relationship('User', back_populates='meal_logs')


class WeightGoal(Base):
    """
    Tracks users' weight goals and progress over time.
    """
    __tablename__ = 'weight_goals'

    id = Column(Integer, primary_key=True)
    current_weight = Column(Float, nullable=False)  # Current weight at record time
    goal_weight = Column(Float, nullable=False)  # Target weight user wants to reach
    difference = Column(Float, nullable=False)  # Difference between current and goal weight
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # Time of record
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Associated user

    user = relationship('User', back_populates='weight_goals')


class WaterIntake(Base):
    """
    Logs daily water intake for users.
    """
    __tablename__ = 'water_intake'

    id = Column(Integer, primary_key=True)
    cups = Column(Integer, nullable=False)  # Number of cups consumed
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # Time of intake
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Associated user

    user = relationship('User', back_populates='water_intakes')

    def __repr__(self):
        return f"<WaterIntake(user_id={self.user_id}, cups={self.cups}, timestamp={self.timestamp})>"


class LoginSession(Base):
    """
    Records user login sessions for tracking purposes.
    """
    __tablename__ = 'login_sessions'

    id = Column(Integer, primary_key=True)
    login_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # Timestamp of login
    ip_address = Column(String(45), nullable=True)  # IP address of the user during login
    user_agent = Column(Text, nullable=True)  # User agent string for device/browser identification
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Associated user

    user = relationship('User', back_populates='login_sessions')
