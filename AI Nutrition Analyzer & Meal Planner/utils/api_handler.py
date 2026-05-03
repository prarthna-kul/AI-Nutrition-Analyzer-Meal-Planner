import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CALORIE_NINJA_API_KEY") or st.secrets["CALORIE_NINJA_API_KEY"]
BASE_URL = "https://api.calorieninjas.com/v1/nutrition"

def get_nutrition(query: str) -> dict:
    """Fetch nutrition data from CalorieNinjas API."""
    if not query.strip():
        return {"error": "Empty query"}
    
    headers = {"X-Api-Key": API_KEY}
    params = {"query": query}

    try:
        response = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("items"):
            return {"error": "No results found. Try a different food name."}
        
        return data
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Check your connection."}
    except requests.exceptions.HTTPError as e:
        return {"error": f"API Error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


def aggregate_nutrition(items: list) -> dict:
    """Sum up macros across multiple food items."""
    totals = {
        "calories": 0, "protein_g": 0,
        "carbohydrates_total_g": 0, "fat_total_g": 0,
        "fiber_g": 0, "sugar_g": 0, "sodium_mg": 0
    }
    for item in items:
        for key in totals:
            totals[key] += item.get(key, 0)
    
    return {k: round(v, 2) for k, v in totals.items()}
