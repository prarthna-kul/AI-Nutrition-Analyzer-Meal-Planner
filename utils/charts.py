import plotly.graph_objects as go
import plotly.express as px

COLORS = {
    "protein": "#6C63FF",
    "carbs": "#F59E0B",
    "fat": "#EF4444",
    "fiber": "#10B981",
    "calories": "#3B82F6"
}

def macro_donut(protein, carbs, fat):
    fig = go.Figure(go.Pie(
        labels=["Protein", "Carbs", "Fat"],
        values=[protein, carbs, fat],
        hole=0.6,
        marker_colors=[COLORS["protein"], COLORS["carbs"], COLORS["fat"]],
        textinfo="label+percent",
        hovertemplate="%{label}: %{value}g<extra></extra>"
    ))
    fig.update_layout(
        showlegend=True,
        margin=dict(t=20, b=20, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )
    return fig


def calorie_gauge(eaten, target):
    pct = min(eaten / target, 1.5) if target else 0
    color = "#10B981" if pct <= 1 else "#EF4444"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=eaten,
        delta={"reference": target, "valueformat": ".0f"},
        gauge={
            "axis": {"range": [0, target * 1.5]},
            "bar": {"color": color},
            "steps": [
                {"range": [0, target * 0.8], "color": "#1E293B"},
                {"range": [target * 0.8, target], "color": "#14532D"},
                {"range": [target, target * 1.5], "color": "#450A0A"},
            ],
            "threshold": {
                "line": {"color": "white", "width": 3},
                "value": target
            }
        },
        title={"text": "Calories (kcal)", "font": {"color": "white"}}
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        margin=dict(t=40, b=10)
    )
    return fig


def macro_bar_comparison(eaten: dict, targets: dict):
    categories = ["Protein (g)", "Carbs (g)", "Fat (g)"]
    eaten_vals = [eaten.get("protein_g", 0), eaten.get("carbohydrates_total_g", 0), eaten.get("fat_total_g", 0)]
    target_vals = [targets.get("protein_g", 0), targets.get("carbs_g", 0), targets.get("fat_g", 0)]
    
    fig = go.Figure(data=[
        go.Bar(name="Eaten", x=categories, y=eaten_vals,
               marker_color=[COLORS["protein"], COLORS["carbs"], COLORS["fat"]], opacity=0.9),
        go.Bar(name="Target", x=categories, y=target_vals,
               marker_color="rgba(255,255,255,0.2)", marker_line_color="white",
               marker_line_width=1.5)
    ])
    fig.update_layout(
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
        margin=dict(t=10, b=10)
    )
    return fig