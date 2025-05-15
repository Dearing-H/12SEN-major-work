from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# ⚠️ NEVER expose your key in production. Use environment variables!
openai.api_key = "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"

class Calculator:
    def __init__(self, age, weight, height, gender, activity):
        self.age = age
        self.weight = weight
        self.height = height
        self.gender = gender.lower()
        self.activity = activity.lower()

    def bmr(self):
        if self.gender == "male":
            return 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        else:
            return 10 * self.weight + 6.25 * self.height - 5 * self.age - 161

    def tdee(self):
        factors = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725,
            "very active": 1.9
        }
        return self.bmr() * factors.get(self.activity, 1.2)

def get_gpt_explanation(age, weight, height, gender, activity, goal, bmr, tdee, target):
    try:
        prompt = (
            f"Explain in simple terms the calorie needs for a {gender.lower()}, age {age}, "
            f"weighing {weight}kg, {height}cm tall, activity level '{activity}', "
            f"with a goal to '{goal}'.\n\n"
            f"The BMR is {bmr:.1f}, TDEE is {tdee:.1f}, and the goal target is {target:.1f} kcal."
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful fitness and nutrition assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"GPT Error: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            age = int(request.form['age'])
            weight = float(request.form['weight'])
            height = float(request.form['height'])
            gender = request.form['gender']
            activity = request.form['activity']
            goal = request.form['goal']

            calc = Calculator(age, weight, height, gender, activity)
            bmr = calc.bmr()
            tdee = calc.tdee()

            if goal.lower() == "cut":
                target = tdee - 500
            elif goal.lower() == "bulk":
                target = tdee + 500
            else:
                target = tdee

            gpt_message = get_gpt_explanation(age, weight, height, gender, activity, goal, bmr, tdee, target)

            return render_template('result.html',
                                   bmr=bmr,
                                   tdee=tdee,
                                   target=target,
                                   gpt_message=gpt_message)

        except Exception as e:
            return render_template('index.html', error=f"Error: {e}")
    return render_template('index.html')