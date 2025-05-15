import tkinter as tk
from tkinter import ttk, messagebox
import openai

#OpenAI API key
openai.api_key = "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"  # 🔒 Never hardcode in production apps!


def get_gpt_explanation(age, weight, height, gender, activity, goal, bmr, tdee, target):
    try:
        prompt = (
            f"Explain in simple terms the calorie needs for a {gender.lower()}, age {age}, "
            f"weighing {weight}kg, {height}cm tall, activity level '{activity}', "
            f"with a goal to '{goal}'.\n\n"
            f"The BMR is {bmr:.1f}, TDEE is {tdee:.1f}, and the goal target is {target:.1f} kcal."
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # use "gpt-4" if you have access
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


def calculate():
    try:
        age = int(age_var.get())
        weight = float(weight_var.get())
        height = float(height_var.get())
        gender = gender_var.get()
        activity = activity_var.get()
        goal = goal_var.get()

        calc = Calculator(age, weight, height, gender, activity)
        bmr = calc.bmr()
        tdee = calc.tdee()

        if goal.lower() == "cut":
            target = tdee - 500
        elif goal.lower() == "bulk":
            target = tdee + 500
        else:
            target = tdee


        gpt_msg = get_gpt_explanation(age, weight, height, gender, activity, goal, bmr, tdee, target)

        #Show Result
        messagebox.showinfo("Calorie Info",
            f"BMR: {bmr:.1f} kcal\nTDEE: {tdee:.1f} kcal\nGoal: {target:.1f} kcal\n\n📘 GPT says:\n{gpt_msg}")

    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")


root = tk.Tk()
root.title("Calorie Calculator + GPT")
root.resizable(False, False)


window_width = 300
window_height = 250
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width - window_width) / 2)
y = int((screen_height - window_height) / 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

#Variables
age_var = tk.StringVar()
weight_var = tk.StringVar()
height_var = tk.StringVar()
gender_var = tk.StringVar(value="Male")
activity_var = tk.StringVar(value="Moderate")
goal_var = tk.StringVar(value="Maintain")

#Layout
ttk.Label(root, text="Age:").grid(row=0, column=0)
ttk.Entry(root, textvariable=age_var).grid(row=0, column=1)

ttk.Label(root, text="Weight (kg):").grid(row=1, column=0)
ttk.Entry(root, textvariable=weight_var).grid(row=1, column=1)

ttk.Label(root, text="Height (cm):").grid(row=2, column=0)
ttk.Entry(root, textvariable=height_var).grid(row=2, column=1)

ttk.Label(root, text="Gender:").grid(row=3, column=0)
ttk.Combobox(root, textvariable=gender_var, values=["Male", "Female"], state="readonly").grid(row=3, column=1)

ttk.Label(root, text="Activity:").grid(row=4, column=0)
ttk.Combobox(root, textvariable=activity_var,
             values=["Sedentary", "Light", "Moderate", "Active", "Very Active"],
             state="readonly").grid(row=4, column=1)

ttk.Label(root, text="Goal:").grid(row=5, column=0)
ttk.Combobox(root, textvariable=goal_var,
             values=["Cut", "Maintain", "Bulk"],
             state="readonly").grid(row=5, column=1)

ttk.Button(root, text="Calculate", command=calculate).grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()