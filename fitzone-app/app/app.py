from flask import Flask, render_template, request, flash, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Gym, BMIR, CalorieRecord, ExerciseLog, MealLog, WaterIntake, WeightGoal, AIWorkoutPlan, DailyNutrition
from datetime import datetime
import os

# --- App Setup ---
app = Flask(__name__)
app.secret_key = "abc123"  # ⚠️ Replace with env var in production

# --- Database Setup ---
# Get the absolute path to the directory where this file is located
basedir = os.path.abspath(os.path.dirname(__file__))
# Create the full path for the database file
db_path = os.path.join(basedir, "FITZONE.db")
engine = create_engine(f"sqlite:///{db_path}", echo=True)
Session = sessionmaker(bind=engine)

# --- New route to save AI-generated workout plans ---
@app.route('/save_ai_workout', methods=["POST"])
def save_ai_workout():
    if 'user_id' not in session:
        return {"status": "unauthorized"}, 401

    data = request.get_json()
    content = data.get("workout_plan")

    if not content:
        return {"status": "error", "message": "No workout content provided"}, 400

    db_session = Session()
    try:
        plan = AIWorkoutPlan(user_id=session['user_id'], content=content)
        db_session.add(plan)
        db_session.commit()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500
    finally:
        db_session.close()

# --- Nutrition Endpoints ---
@app.route('/save_nutrition', methods=['POST'])
def save_nutrition():
    if 'user_id' not in session:
        return {"status": "unauthorized"}, 401

    data = request.get_json()
    db_session = Session()
    try:
        nutrition = DailyNutrition(
            user_id=session['user_id'],
            date=datetime.utcnow().date(),
            calories=data.get('calories'),
            protein=data.get('protein'),
            carbs=data.get('carbs'),
            fats=data.get('fats')
        )
        db_session.add(nutrition)
        db_session.commit()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500
    finally:
        db_session.close()


@app.route('/get_nutrition_summary')
def get_nutrition_summary():
    if 'user_id' not in session:
        return {"status": "unauthorized"}, 401

    db_session = Session()
    try:
        today = datetime.utcnow().date()
        summary = db_session.query(DailyNutrition).filter_by(user_id=session['user_id'], date=today).first()

        if summary:
            return {
                "calories": summary.calories,
                "protein": summary.protein,
                "carbs": summary.carbs,
                "fats": summary.fats
            }
        else:
            return {"calories": 0, "protein": 0, "carbs": 0, "fats": 0}
    finally:
        db_session.close()

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign_up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm_password")

        if not all([username, password, confirm]):
            flash("All fields are required.", "danger")
            return render_template("sign_up.html")

        if password != confirm:
            flash("Passwords do not match", "danger")
            return render_template("sign_up.html")

        db_session = Session()
        try:
            if db_session.query(User).filter_by(username=username).first():
                flash("Username already exists", "danger")
                return render_template("sign_up.html")

            new_user = User(username=username, password=generate_password_hash(password))
            db_session.add(new_user)
            db_session.commit()

            flash("Sign-up successful. Please log in.", "success")
            return redirect(url_for('login'))
        finally:
            db_session.close()

    return render_template("sign_up.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        db_session = Session()
        try:
            user = db_session.query(User).filter_by(username=username).first()

            if user and check_password_hash(user.password, password):
                session['user'] = username
                session['user_id'] = user.id
                flash("Login successful!", "success")
                return redirect(url_for('dashboard'))

            flash("Invalid username or password", "danger")
        finally:
            db_session.close()

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for('login'))

@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    if 'user' not in session:
        flash("Please log in to access the dashboard", "warning")
        return redirect(url_for('login'))

    db_session = Session()
    try:
        user = db_session.query(User).filter_by(username=session['user']).first()
        if not user:
            session.clear()
            flash("User not found", "danger")
            return redirect(url_for('login'))

        if request.method == "POST":
            try:
                # BMI
                if "bmi_submit" in request.form:
                    weight = float(request.form.get("weight"))
                    height = float(request.form.get("height"))
                    bmi = round(weight / ((height / 100) ** 2), 2)
                    
                    # Add to history
                    db_session.add(BMIR(user_id=user.id, weight=weight, height=height, bmi=bmi))
                    
                    # Update user's current stats
                    user.weight = weight
                    user.height = height
                    user.bmi = bmi
                    
                    db_session.commit()
                    flash(f"BMI saved: {bmi}", "success")
                    return redirect(url_for('dashboard') + '#bmi')

                # Calories
                elif "calorie_submit" in request.form:
                    age = int(request.form.get("age"))
                    weight = float(request.form.get("c_weight"))
                    height = float(request.form.get("c_height"))
                    activity = float(request.form.get("activity"))
                    bmr = 10 * weight + 6.25 * height - 5 * age + 5
                    tdee = int(bmr * activity)

                    # Add to history
                    db_session.add(CalorieRecord(user_id=user.id, age=age, weight=weight, height=height,
                                                 activity_level=activity, tdee=tdee))

                    # Update user's current stats
                    user.age = age
                    user.weight = weight
                    user.height = height
                    user.activity_level = activity
                    user.tdee = tdee

                    db_session.commit()
                    flash(f"TDEE saved: {tdee} calories/day", "success")
                    return redirect(url_for('dashboard') + '#calories')

                # Exercise
                elif "exercise_submit" in request.form:
                    name = request.form.get("exercise")
                    reps = int(request.form.get("reps"))
                    sets = int(request.form.get("sets"))
                    total = reps * sets

                    # Add to history
                    db_session.add(ExerciseLog(user_id=user.id, exercise_name=name, reps=reps, sets=sets, total_reps=total))

                    # Update user's last exercise
                    user.last_exercise_name = name
                    user.last_reps = reps
                    user.last_sets = sets

                    db_session.commit()
                    flash(f"Exercise saved: {total} total reps", "success")
                    return redirect(url_for('dashboard') + '#reps')

                # Meal
                elif "meal_submit" in request.form:
                    meal = request.form.get("meal")
                    db_session.add(MealLog(user_id=user.id, meal_description=meal))
                    user.last_meal_description = meal
                    db_session.commit()
                    flash("Meal logged.", "success")
                    return redirect(url_for('dashboard') + '#meals')

                # Goals
                elif "goal_submit" in request.form:
                    current_weight = float(request.form.get("current_weight"))
                    goal_weight = float(request.form.get("goal_weight"))
                    difference = goal_weight - current_weight
                    
                    db_session.add(WeightGoal(user_id=user.id, current_weight=current_weight, goal_weight=goal_weight, difference=difference))
                    
                    user.current_weight = current_weight
                    user.goal_weight = goal_weight
                    db_session.commit()
                    flash("Weight goal saved.", "success")
                    return redirect(url_for('dashboard') + '#goals')

                # Water
                elif "water_submit" in request.form:
                    cups = int(request.form.get("cups"))
                    db_session.add(WaterIntake(user_id=user.id, cups=cups))
                    db_session.commit()
                    flash(f"Water intake saved: {cups} cups", "success")
                    return redirect(url_for('dashboard') + '#water')

            except Exception as e:
                flash(f"Error: {str(e)}", "danger")

        # Query latest records for the logged-in user
        bmi_records = db_session.query(BMIR).filter_by(user_id=user.id).order_by(BMIR.id.desc()).limit(5).all()
        calorie_records = db_session.query(CalorieRecord).filter_by(user_id=user.id).order_by(CalorieRecord.id.desc()).limit(5).all()
        exercise_logs = db_session.query(ExerciseLog).filter_by(user_id=user.id).order_by(ExerciseLog.id.desc()).limit(5).all()
        meal_logs = db_session.query(MealLog).filter_by(user_id=user.id).order_by(MealLog.id.desc()).limit(5).all()
        water_logs = db_session.query(WaterIntake).filter_by(user_id=user.id).order_by(WaterIntake.id.desc()).limit(5).all()

        # Prepare data for progress chart
        recent_exercise = db_session.query(ExerciseLog).filter_by(user_id=user.id).order_by(ExerciseLog.id.desc()).limit(4).all()
        recent_weights = db_session.query(BMIR).filter_by(user_id=user.id).order_by(BMIR.id.desc()).limit(4).all()

        progress_labels = [log.date.strftime('%b %d') if hasattr(log, 'date') else f'Entry {i+1}' for i, log in enumerate(reversed(recent_exercise))]
        progress_reps = [log.total_reps for log in reversed(recent_exercise)]
        progress_weight = [log.weight for log in reversed(recent_weights)]

        return render_template(
            "dashboard.html",
            user=user,
            bmi_records=bmi_records,
            calorie_records=calorie_records,
            exercise_logs=exercise_logs,
            meal_logs=meal_logs,
            water_logs=water_logs,
            progress_labels=progress_labels,
            progress_reps=progress_reps,
            progress_weight=progress_weight
        )
    finally:
        db_session.close()

# --- Run App ---
if __name__ == '__main__':
    with app.app_context():
        Base.metadata.create_all(engine)
    app.run(debug=True)
@app.route('/about')
def about():
    return render_template('about.html')
