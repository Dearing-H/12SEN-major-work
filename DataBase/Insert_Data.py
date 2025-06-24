from datetime import date
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash
from setup_db import User, Gym

# Connect to the database
engine = create_engine('sqlite:///FITZONE.db')
Session = sessionmaker(bind=engine)
session = Session()
# Insert users with hashed passwords
user1 = User(username='john_doe',
password=generate_password_hash('password123'))
user2 = User(username='jane_doe',
password=generate_password_hash('mypassword'))
user3 = User(username='admin',
password=generate_password_hash('123'))
user4 = User(username='guest_preview',
password=generate_password_hash('password123'))
session.add(user1)
session.add(user2)
session.add(user3)
session.add(user4)
session.commit()

# Insert tasks
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
session.add(gym1)
session.add(gym2)
session.commit()
print("Users and gym sessions inserted successfully.")