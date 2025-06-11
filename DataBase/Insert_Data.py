# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
# from werkzeug.security import generate_password_hash
# from setup_db import User, Gym


# # Connect to the database
# engine = create_engine('sqlite:///todo.db')
# Session = sessionmaker(bind=engine)
# session = Session()
# # Insert users with hashed passwords
# user1 = User(username='john_doe',
# password=generate_password_hash('password123'))
# user2 = User(username='jane_doe',
# password=generate_password_hash('mypassword'))
# session.add(User1)
# session.add(User2)
# session.commit()
# # Insert tasks
# task1 = ToDo(task='Learn SQLAlchemy', done=False, user_id=user1.id)
# task2 = ToDo(task='Build an app', done=False, user_id=user2.id)
# session.add(task1)
# session.add(task2)
# session.commit()
# print("Users and tasks inserted successfully.")