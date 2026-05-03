import json
import os

def calculate_tdee(weight_kg, height_cm, age, gender, activity_level):
    """Harris-Benedict BMR + activity multiplier."""
    if gender == "Male":
        bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)

    multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Extra Active": 1.9
    }
    return round(bmr * multipliers.get(activity_level, 1.2))


def get_calorie_target(tdee, goal):
    """Adjust calories based on goal."""
    adjustments = {
        "Weight Loss": -500,
        "Muscle Gain": +300,
        "Maintenance": 0,
        "Recomposition": 0
    }
    return tdee + adjustments.get(goal, 0)


def get_macro_split(calories, goal):
    """Return macros in grams based on goal."""
    splits = {
        "Weight Loss":    {"protein": 0.40, "carbs": 0.30, "fat": 0.30},
        "Muscle Gain":    {"protein": 0.35, "carbs": 0.45, "fat": 0.20},
        "Maintenance":    {"protein": 0.30, "carbs": 0.40, "fat": 0.30},
        "Recomposition":  {"protein": 0.40, "carbs": 0.35, "fat": 0.25},
    }
    s = splits.get(goal, splits["Maintenance"])
    return {
        "protein_g":  round((calories * s["protein"]) / 4),
        "carbs_g":    round((calories * s["carbs"]) / 4),
        "fat_g":      round((calories * s["fat"]) / 9),
    }


def load_meal_templates():
    path = os.path.join(os.path.dirname(__file__), "../data/meal_templates.json")
    with open(path, "r") as f:
        return json.load(f)


def generate_meal_plan(goal, calorie_target):
    """Return a 1-day meal plan from templates, scaled to calorie target."""
    templates = load_meal_templates()
    plan = templates.get(goal, templates["Maintenance"])
    
    # Scale portions proportionally
    base_calories = sum(m["calories"] for m in plan)
    scale = calorie_target / base_calories if base_calories else 1.0

    scaled = []
    for meal in plan:
        scaled.append({
            **meal,
            "calories": round(meal["calories"] * scale),
            "protein_g": round(meal["protein_g"] * scale, 1),
            "carbs_g":   round(meal["carbs_g"] * scale, 1),
            "fat_g":     round(meal["fat_g"] * scale, 1),
        })
    return scaled