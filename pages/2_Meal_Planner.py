import streamlit as st
from utils.meal_logic import calculate_tdee, get_calorie_target, get_macro_split, generate_meal_plan

if "meal_plan" not in st.session_state:
    st.session_state.meal_plan = None

st.set_page_config(page_title="Meal Planner", page_icon="🍽️", layout="wide")

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🍽️ Goal-Based Meal Planner")
st.caption("Enter your profile to get a personalized daily meal plan with macro targets")

# ─── Profile Form ─────────────────────────────────────────────────────────────
with st.form("profile_form"):
    st.subheader("Your Profile")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        name   = st.text_input("Name", placeholder="Your name")
        age    = st.number_input("Age", 10, 100, 25)
        gender = st.selectbox("Gender", ["Male", "Female"])
    with col2:
        weight = st.number_input("Weight (kg)", 30.0, 200.0, 70.0, step=0.5)
        height = st.number_input("Height (cm)", 100.0, 250.0, 170.0, step=0.5)
    with col3:
        activity = st.selectbox("Activity Level", [
            "Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"
        ])
        goal = st.selectbox("Fitness Goal", ["Weight Loss", "Muscle Gain", "Maintenance", "Recomposition"])
    
    submitted = st.form_submit_button("Generate My Plan 🎯", use_container_width=True)

if submitted:
    tdee     = calculate_tdee(weight, height, age, gender, activity)
    cal_tgt  = get_calorie_target(tdee, goal)
    macros   = get_macro_split(cal_tgt, goal)
    plan     = generate_meal_plan(goal, cal_tgt)

    # Save to session
    st.session_state.update({
        "user_profile": {"name": name, "age": age, "gender": gender,
                         "weight": weight, "height": height, "activity": activity},
        "goal":           goal,
        "calorie_target": cal_tgt,
        "macro_targets":  macros,
        "meal_plan":      plan,
        "tdee":           tdee
    })

    st.success(f"✅ Plan generated for {name or 'you'}!")

    # ─── Targets Banner ───────────────────────────────────────────────────────
    st.subheader("📊 Your Daily Targets")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("TDEE",        f"{tdee} kcal", help="Total Daily Energy Expenditure")
    c2.metric("Target",      f"{cal_tgt} kcal")
    c3.metric("Protein",     f"{macros['protein_g']}g")
    c4.metric("Carbs",       f"{macros['carbs_g']}g")
    c5.metric("Fat",         f"{macros['fat_g']}g")

    # ─── Meal Plan Table ──────────────────────────────────────────────────────
    st.subheader(f"🗓️ Meal Plan — {goal}")
    for meal in plan:
        with st.expander(f"🍴 {meal['meal']}  —  {meal['calories']} kcal"):
            st.markdown(f"**{meal['food']}**")
            mc1, mc2, mc3 = st.columns(3)
            mc1.metric("Protein", f"{meal['protein_g']}g")
            mc2.metric("Carbs",   f"{meal['carbs_g']}g")
            mc3.metric("Fat",     f"{meal['fat_g']}g")

elif st.session_state.meal_plan:
    st.info("📋 Showing previously generated plan. Re-submit to regenerate.")
    for meal in st.session_state.meal_plan:
        with st.expander(f"🍴 {meal['meal']}  —  {meal['calories']} kcal"):
            st.markdown(f"**{meal['food']}**")
