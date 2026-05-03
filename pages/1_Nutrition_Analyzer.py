import streamlit as st
import pandas as pd
from utils.api_handler import get_nutrition, aggregate_nutrition
from utils.charts import macro_donut

if "nutrition_log" not in st.session_state:
    st.session_state.nutrition_log = []
st.set_page_config(page_title="Nutrition Analyzer", page_icon="🔬", layout="wide")

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🔬 Real-Time Nutrition Analyzer")
st.caption("Powered by CalorieNinjas API — Analyze any food, ingredient, or full meal")

# ─── Input ────────────────────────────────────────────────────────────────────
query = st.text_input(
    "Enter food(s) to analyze",
    placeholder="e.g. 2 eggs, 100g oats, 1 cup milk",
    help="You can enter multiple items separated by commas"
)

col1, col2 = st.columns([1, 4])
with col1:
    analyze_btn = st.button("Analyze 🚀", use_container_width=True)
with col2:
    log_btn = st.button("+ Add to Daily Log", use_container_width=False)

if analyze_btn and query:
    with st.spinner("Fetching nutrition data..."):
        result = get_nutrition(query)

    if "error" in result:
        st.error(result["error"])
    else:
        items = result["items"]
        totals = aggregate_nutrition(items)
        st.session_state["_last_analyzed"] = {"items": items, "totals": totals, "query": query}

        st.success(f"Found {len(items)} item(s)")

        # ─── Metrics Row ───────────────────────────────────────────────────────
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("🔥 Calories", f"{totals['calories']} kcal")
        c2.metric("🥩 Protein",  f"{totals['protein_g']}g")
        c3.metric("🍞 Carbs",    f"{totals['carbohydrates_total_g']}g")
        c4.metric("🥑 Fat",      f"{totals['fat_total_g']}g")
        c5.metric("🌾 Fiber",    f"{totals['fiber_g']}g")

        # ─── Charts ─────────────────────────────────────────────────────────
        col_chart, col_table = st.columns([1, 1])
        with col_chart:
            st.subheader("Macro Breakdown")
            fig = macro_donut(totals["protein_g"], totals["carbohydrates_total_g"], totals["fat_total_g"])
            st.plotly_chart(fig, use_container_width=True)

        with col_table:
            st.subheader("Per Item Details")
            df = pd.DataFrame(items)[["name", "calories", "protein_g", "carbohydrates_total_g", "fat_total_g", "fiber_g", "sugar_g"]]
            df.columns = ["Food", "Calories", "Protein (g)", "Carbs (g)", "Fat (g)", "Fiber (g)", "Sugar (g)"]
            st.dataframe(df.style.format("{:.1f}", subset=df.columns[1:]), use_container_width=True)

# ─── Log Button ───────────────────────────────────────────────────────────────
if log_btn and "_last_analyzed" in st.session_state:
    last = st.session_state["_last_analyzed"]
    st.session_state.nutrition_log.extend(last["items"])
    st.toast(f"✅ Added {len(last['items'])} item(s) to daily log!", icon="🥗")

# ─── Daily Log ────────────────────────────────────────────────────────────────
if st.session_state.nutrition_log:
    st.divider()
    st.subheader(f"📋 Today's Food Log ({len(st.session_state.nutrition_log)} items)")
    
    totals_log = aggregate_nutrition(st.session_state.nutrition_log)
    log_df = pd.DataFrame(st.session_state.nutrition_log)[["name", "calories", "protein_g", "carbohydrates_total_g", "fat_total_g"]]
    log_df.columns = ["Food", "Calories", "Protein (g)", "Carbs (g)", "Fat (g)"]
    st.dataframe(log_df, use_container_width=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Calories", f"{totals_log['calories']} kcal")
    c2.metric("Total Protein",  f"{totals_log['protein_g']}g")
    c3.metric("Total Carbs",    f"{totals_log['carbohydrates_total_g']}g")
    c4.metric("Total Fat",      f"{totals_log['fat_total_g']}g")

    if st.button("🗑️ Clear Log"):
        st.session_state.nutrition_log = []
        st.rerun()
