import streamlit as st

st.set_page_config(
    page_title="NutriAI — Nutrition Analyzer",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Session state defaults
defaults = {
    "user_profile": {},
    "nutrition_log": [],
    "meal_plan": [],
    "goal": "Maintenance",
    "calorie_target": 2000,
    "macro_targets": {"protein_g": 150, "carbs_g": 200, "fat_g": 65}
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── HOME PAGE ────────────────────────────────────────────────────────────────

st.markdown("""
<div style='text-align:center; padding: 40px 0 20px'>
    <h1 style='
    font-size:3.5rem;
    font-weight:800;
    margin:0;
    background: linear-gradient(135deg, #6C63FF 0%, #EC4899 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: #6C63FF;  /* fallback color */
'>
    NutriAI
</h1>
    <p style='color:#64748B; font-size:1.15rem; margin-top:10px; font-weight:400;'>
        Real-time nutrition analysis · Goal-based meal planning · Personalized insights
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🔬 Foods Analyzed", len(st.session_state.nutrition_log), delta=None)
with col2:
    total_cals = sum(i.get("calories", 0) for i in st.session_state.nutrition_log)
    st.metric("🔥 Total Calories", f"{round(total_cals)} kcal")
with col3:
    st.metric("🎯 Current Goal", st.session_state.goal)
with col4:
    st.metric("📋 Meals Planned", len(st.session_state.meal_plan))

st.divider()

st.markdown("""
### 👆 Get Started
Use the **sidebar** to navigate between modules:
- **🔬 Nutrition Analyzer** — Enter any food or meal to get instant macro breakdown
- **🍽️ Meal Planner** — Set your profile and generate a personalized daily plan
- **📊 Dashboard** — Visual overview of your calories, macros, and recommendations
""")