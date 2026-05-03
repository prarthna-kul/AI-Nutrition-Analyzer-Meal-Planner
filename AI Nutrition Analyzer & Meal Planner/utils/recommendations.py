def generate_recommendations(macros_eaten, macro_targets, goal):
    recs = []
    
    protein_eaten = macros_eaten.get("protein_g", 0)
    protein_target = macro_targets.get("protein_g", 1)
    carbs_eaten = macros_eaten.get("carbohydrates_total_g", 0)
    carbs_target = macro_targets.get("carbs_g", 1)
    fat_eaten = macros_eaten.get("fat_total_g", 0)
    fat_target = macro_targets.get("fat_g", 1)
    calories = macros_eaten.get("calories", 0)

    # Protein feedback
    pct = protein_eaten / protein_target
    if pct < 0.7:
        recs.append(("🥩", "Protein Deficit", f"You're at {round(pct*100)}% of protein target. Add chicken breast, Greek yogurt, or eggs."))
    elif pct > 1.3:
        recs.append(("⚠️", "Protein Excess", "Protein is quite high. Balance with more complex carbs."))
    else:
        recs.append(("✅", "Protein On Track", f"Great job! {protein_eaten}g / {protein_target}g target met."))

    # Goal-specific
    if goal == "Weight Loss" and calories > 2500:
        recs.append(("🔥", "Calorie Alert", "You've exceeded typical weight loss range. Consider reducing portion sizes."))
    if goal == "Muscle Gain" and calories < 2000:
        recs.append(("💪", "Calorie Too Low", "For muscle gain, aim for a calorie surplus. Add a protein shake or nut butter."))

    # Hydration
    recs.append(("💧", "Hydration Reminder", "Drink at least 8–10 glasses of water today, especially if training."))

    # Fiber
    fiber = macros_eaten.get("fiber_g", 0)
    if fiber < 15:
        recs.append(("🥦", "Low Fiber", "Add vegetables, legumes, or oats to boost fiber intake."))

    return recs