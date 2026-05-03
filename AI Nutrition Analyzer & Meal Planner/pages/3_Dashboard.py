import streamlit as st
from utils.api_handler import aggregate_nutrition
from utils.charts import calorie_gauge, macro_bar_comparison, macro_donut
from utils.recommendations import generate_recommendations

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("📊 Analytics Dashboard")

if not st.session_state.get("nutrition_log") and not st.session_state.get("meal_plan"):
    st.warning("⚠️ No data yet! Go to **Nutrition Analyzer** and log some food first.")
    st.stop()

goal         = st.session_state.get("goal", "Maintenance")
cal_target   = st.session_state.get("calorie_target", 2000)
macro_tgts   = st.session_state.get("macro_targets", {"protein_g": 150, "carbs_g": 200, "fat_g": 65})
log          = st.session_state.get("nutrition_log", [])
eaten        = aggregate_nutrition(log) if log else {k: 0 for k in ["calories","protein_g","carbohydrates_total_g","fat_total_g","fiber_g"]}

# ─── Row 1: Calorie gauge + Macro donut ───────────────────────────────────────
col1, col2 = st.columns([1, 1])
with col1:
    st.subheader("🔥 Calorie Progress")
    st.plotly_chart(calorie_gauge(eaten["calories"], cal_target), use_container_width=True)

with col2:
    st.subheader("🥗 Macro Distribution")
    st.plotly_chart(
        macro_donut(eaten["protein_g"], eaten["carbohydrates_total_g"], eaten["fat_total_g"]),
        use_container_width=True
    )

# ─── Row 2: Bar comparison ────────────────────────────────────────────────────
st.subheader("📈 Eaten vs Target — Macros")
st.plotly_chart(macro_bar_comparison(eaten, macro_tgts), use_container_width=True)

# ─── Row 3: Recommendations ───────────────────────────────────────────────────
st.subheader("💡 Personalized Recommendations")
recs = generate_recommendations(eaten, macro_tgts, goal)

cols = st.columns(min(len(recs), 3))
for i, (icon, title, body) in enumerate(recs):
    with cols[i % 3]:
        st.markdown(f"""
<div style='background:#FFFFFF; border-radius:12px; padding:16px; margin-bottom:12px;
            border:1px solid #E2E8F0; box-shadow:0 2px 8px rgba(0,0,0,0.05)'>
    <div style='font-size:1.8rem'>{icon}</div>
    <div style='font-weight:700; margin:6px 0 4px; color:#1E293B'>{title}</div>
    <div style='color:#64748B; font-size:0.9rem'>{body}</div>
</div>
""", unsafe_allow_html=True)
# ─── Meal Plan Summary ────────────────────────────────────────────────────────
if st.session_state.meal_plan:
    st.divider()
    st.subheader("🗓️ Today's Meal Plan Summary")
    plan = st.session_state.meal_plan
    for m in plan:
        prog = m["calories"] / cal_target
        st.markdown(f"**{m['meal']}** — {m['food']} &nbsp;&nbsp; `{m['calories']} kcal`")
        st.progress(min(prog, 1.0))