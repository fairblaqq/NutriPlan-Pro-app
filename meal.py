import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

# Page Setup
st.set_page_config(
    page_title="NutriPlan Pro",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main { background-color: #f4f6f9; }
    h1 { color: #1e5249; font-family: 'Inter', sans-serif; font-weight: 800; }
    h2, h3 { color: #2c3e50; font-family: 'Inter', sans-serif; }
    .metric-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #eef2f5;
        text-align: center;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
    .meal-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #1e5249;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
</style>
""", unsafe_allow_html=True)

# --- FOOD DATABASE ---
# Tags: V = Vegan, K = Keto, GF = Gluten-Free, NF = Nut-Free
@st.cache_data
def get_master_food_db():
    return [
        # Breakfast
        {"id": 101, "name": "Oatmeal with Sliced Bananas", "calories": 350, "protein": 12, "carbs": 60, "fats": 6, "category": "Breakfast", "tags": ["V", "GF", "NF"], "ingredients": ["Rolled Oats", "Banana", "Almond Milk", "Chia Seeds"], "aisle": "Pantry"},
        {"id": 102, "name": "Scrambled Eggs & Avocado Toast", "calories": 420, "protein": 18, "carbs": 32, "fats": 22, "category": "Breakfast", "tags": ["NF"], "ingredients": ["Eggs", "Whole Wheat Bread", "Avocado", "Olive Oil"], "aisle": "Produce"},
        {"id": 103, "name": "Keto Almond Flour Pancakes", "calories": 490, "protein": 16, "carbs": 12, "fats": 41, "category": "Breakfast", "tags": ["K", "GF"], "ingredients": ["Almond Flour", "Eggs", "Erythritol", "Butter"], "aisle": "Pantry"},
        {"id": 104, "name": "Vegan Tofu Scramble with Spinach", "calories": 290, "protein": 20, "carbs": 10, "fats": 16, "category": "Breakfast", "tags": ["V", "GF", "NF"], "ingredients": ["Firm Tofu", "Spinach", "Turmeric", "Bell Peppers"], "aisle": "Produce"},
        {"id": 105, "name": "Greek Yogurt & Walnut Parfait", "calories": 310, "protein": 17, "carbs": 24, "fats": 15, "category": "Breakfast", "tags": ["GF"], "ingredients": ["Greek Yogurt", "Walnuts", "Honey", "Mixed Berries"], "aisle": "Dairy"},
        
        # Lunch
        {"id": 201, "name": "Grilled Chicken & Quinoa Bowl", "calories": 550, "protein": 42, "carbs": 55, "fats": 12, "category": "Lunch", "tags": ["GF", "NF"], "ingredients": ["Chicken Breast", "Quinoa", "Broccoli", "Olive Oil"], "aisle": "Meat"},
        {"id": 202, "name": "Smoked Salmon & Asparagus Salad", "calories": 460, "protein": 36, "carbs": 8, "fats": 32, "category": "Lunch", "tags": ["K", "GF", "NF"], "ingredients": ["Smoked Salmon", "Asparagus", "Mixed Greens", "Lemon Dressing"], "aisle": "Seafood"},
        {"id": 203, "name": "Lentil & Vegetable Curry", "calories": 480, "protein": 22, "carbs": 70, "fats": 9, "category": "Lunch", "tags": ["V", "GF", "NF"], "ingredients": ["Brown Lentils", "Coconut Milk", "Carrots", "Curry Powder"], "aisle": "Pantry"},
        {"id": 204, "name": "Keto Avocado Turkey Wraps", "calories": 510, "protein": 38, "carbs": 6, "fats": 38, "category": "Lunch", "tags": ["K", "GF", "NF"], "ingredients": ["Turkey Breast", "Lettuce Leaves", "Avocado", "Mayonnaise"], "aisle": "Meat"},
        {"id": 205, "name": "Mediterranean Chickpea Salad", "calories": 410, "protein": 14, "carbs": 52, "fats": 14, "category": "Lunch", "tags": ["V", "GF", "NF"], "ingredients": ["Canned Chickpeas", "Cucumber", "Cherry Tomatoes", "Olive Oil"], "aisle": "Produce"},
        
        # Dinner
        {"id": 301, "name": "Baked Cod & Roasted Sweet Potato", "calories": 480, "protein": 34, "carbs": 48, "fats": 10, "category": "Dinner", "tags": ["GF", "NF"], "ingredients": ["Cod Fillet", "Sweet Potato", "Zucchini", "Coconut Oil"], "aisle": "Seafood"},
        {"id": 302, "name": "Premium Garlic Butter Ribeye Steak", "calories": 720, "protein": 52, "carbs": 2, "fats": 56, "category": "Dinner", "tags": ["K", "GF", "NF"], "ingredients": ["Ribeye Steak", "Butter", "Garlic", "Asparagus"], "aisle": "Meat"},
        {"id": 303, "name": "Vegan Chickpea Pasta Marinara", "calories": 520, "protein": 21, "carbs": 78, "fats": 8, "category": "Dinner", "tags": ["V", "GF", "NF"], "ingredients": ["Chickpea Pasta", "Marinara Sauce", "Nutritional Yeast", "Garlic"], "aisle": "Pantry"},
        {"id": 304, "name": "Baked Tofu, Rice & Green Beans", "calories": 460, "protein": 24, "carbs": 62, "fats": 12, "category": "Dinner", "tags": ["V", "GF", "NF"], "ingredients": ["Tofu", "Brown Rice", "Green Beans", "Sesame Oil"], "aisle": "Produce"},
        {"id": 305, "name": "Grilled Lemon-Herb Salmon", "calories": 580, "protein": 40, "carbs": 4, "fats": 42, "category": "Dinner", "tags": ["K", "GF", "NF"], "ingredients": ["Salmon Fillet", "Lemon", "Dill", "Olive Oil"], "aisle": "Seafood"},

        # Snacks
        {"id": 401, "name": "Handful of Mixed Almonds", "calories": 160, "protein": 6, "carbs": 6, "fats": 14, "category": "Snack", "tags": ["K", "V", "GF"], "ingredients": ["Almonds", "Sea Salt"], "aisle": "Pantry"},
        {"id": 402, "name": "Celery Sticks with Peanut Butter", "calories": 190, "protein": 7, "carbs": 8, "fats": 16, "category": "Snack", "tags": ["K", "GF"], "ingredients": ["Celery", "Peanut Butter"], "aisle": "Produce"},
        {"id": 403, "name": "Mixed Berries Bowl", "calories": 80, "protein": 1, "carbs": 18, "fats": 0, "category": "Snack", "tags": ["V", "GF", "NF"], "ingredients": ["Blueberries", "Raspberries", "Strawberries"], "aisle": "Produce"},
        {"id": 404, "name": "Boiled Eggs with Salt & Pepper", "calories": 140, "protein": 12, "carbs": 1, "fats": 10, "category": "Snack", "tags": ["K", "GF", "NF"], "ingredients": ["Eggs"], "aisle": "Dairy"}
    ]

# --- INITIALIZE SESSION STATE ---
if "profile_saved" not in st.session_state:
    st.session_state.profile_saved = False
if "weekly_plan" not in st.session_state:
    st.session_state.weekly_plan = {}
if "custom_recipes" not in st.session_state:
    st.session_state.custom_recipes = []
if "grocery_checklist" not in st.session_state:
    st.session_state.grocery_checklist = {}
if "manual_groceries" not in st.session_state:
    st.session_state.manual_groceries = []
if "water_intake" not in st.session_state:
    st.session_state.water_intake = 0
if "logged_meals" not in st.session_state:
    st.session_state.logged_meals = []
if "weight_history" not in st.session_state:
    st.session_state.weight_history = pd.DataFrame([
        {"Date": (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d"), "Weight": 82.5},
        {"Date": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"), "Weight": 81.8},
        {"Date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"), "Weight": 81.2},
    ])
if "steps_synced" not in st.session_state:
    st.session_state.steps_synced = 4320

# --- HELPER FUNCTIONS ---
def get_filtered_meals(category, tags_to_avoid, tags_to_require):
    db = get_master_food_db() + st.session_state.custom_recipes
    eligible = []
    for item in db:
        if item["category"] != category:
            continue
        
        # Check allergies/restrictions to avoid
        clash = False
        for tag in tags_to_avoid:
            if tag == "V" and "V" not in item["tags"]:
                # If vegan requested but not marked, skip
                clash = True
            if tag == "K" and "K" not in item["tags"]:
                # If keto requested but not marked, skip
                clash = True
            if tag == "GF" and "GF" not in item["tags"]:
                clash = True
            if tag == "NF" and "NF" not in item["tags"]:
                clash = True
        
        if not clash:
            eligible.append(item)
            
    return eligible if eligible else [item for item in db if item["category"] == category]

def generate_weekly_meal_plan(target_cal, tags_to_avoid):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    new_plan = {}
    
    # Split targets
    b_tgt, l_tgt, d_tgt, s_tgt = target_cal*0.25, target_cal*0.35, target_cal*0.30, target_cal*0.10
    
    for day in days:
        breakfasts = get_filtered_meals("Breakfast", tags_to_avoid, [])
        lunches = get_filtered_meals("Lunch", tags_to_avoid, [])
        dinners = get_filtered_meals("Dinner", tags_to_avoid, [])
        snacks = get_filtered_meals("Snack", tags_to_avoid, [])
        
        new_plan[day] = {
            "Breakfast": min(breakfasts, key=lambda x: abs(x["calories"] - b_tgt)),
            "Lunch": min(lunches, key=lambda x: abs(x["calories"] - l_tgt)),
            "Dinner": min(dinners, key=lambda x: abs(x["calories"] - d_tgt)),
            "Snack": min(snacks, key=lambda x: abs(x["calories"] - s_tgt))
        }
    st.session_state.weekly_plan = new_plan

# --- HEADER SECTION ---
col_logo, col_title = st.columns([1, 8])
with col_title:
    st.title("🥗 NutriPlan Pro")
    st.write("Modular, Clinical-Grade Personalized Nutrition & Micro-Targeting Platform")

# --- SIDEBAR: ONBOARDING & BIOMETRICS ENGINE ---
st.sidebar.header("👤 1. User Profiling")
gender = st.sidebar.radio("Biological Gender", ["Male", "Female"])
age = st.sidebar.slider("Age (years)", 15, 85, 28)
weight = st.sidebar.number_input("Weight (kg)", 35.0, 220.0, 80.0, 0.1)
height = st.sidebar.number_input("Height (cm)", 100.0, 240.0, 175.0, 0.5)

activity_level = st.sidebar.selectbox(
    "Physical Activity Level",
    ["Sedentary (desk job)", "Light Activity (1-2 days/wk)", "Moderate Activity (3-5 days/wk)", "Highly Active (Daily/Athletic)"]
)

goal = st.sidebar.selectbox("Health & Weight Goal", ["Lose Weight", "Maintain Weight", "Muscle Gain (Surplus)"])

# Dietary Preference Tags
st.sidebar.markdown("### 🚫 Allergies & Diets")
avoid_tags = []
if st.sidebar.checkbox("Keto Diet Required (High Fat/Low Carb)"):
    avoid_tags.append("K")
if st.sidebar.checkbox("Vegan (Plant-Based only)"):
    avoid_tags.append("V")
if st.sidebar.checkbox("Gluten-Free"):
    avoid_tags.append("GF")
if st.sidebar.checkbox("Strict Nut Allergy"):
    avoid_tags.append("NF")

# Calculation Engine (Mifflin-St Jeor)
if gender == "Male":
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
else:
    bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

af_map = {
    "Sedentary (desk job)": 1.2,
    "Light Activity (1-2 days/wk)": 1.375,
    "Moderate Activity (3-5 days/wk)": 1.55,
    "Highly Active (Daily/Athletic)": 1.725
}
tdee = bmr * af_map[activity_level]

if goal == "Lose Weight":
    target_calories = tdee - 500
elif goal == "Muscle Gain (Surplus)":
    target_calories = tdee + 400
else:
    target_calories = tdee

# Dynamic Macronutrient Allocations
if "K" in avoid_tags:
    p_pct, c_pct, f_pct = 0.25, 0.05, 0.70  # Keto distribution
else:
    p_pct, c_pct, f_pct = 0.30, 0.45, 0.25  # Balanced High-Protein

protein_g = (target_calories * p_pct) / 4
carbs_g = (target_calories * c_pct) / 4
fats_g = (target_calories * f_pct) / 9

if st.sidebar.button("💾 Generate & Sync New Profile"):
    st.session_state.profile_saved = True
    generate_weekly_meal_plan(target_calories, avoid_tags)
    st.sidebar.success("New custom meal plan generated successfully!")

# --- APP SYSTEM MAIN PAGE (TABS SETUP) ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📅 Weekly Meal Planner", 
    "🛒 Automated Grocery Builder", 
    "💧 Logging & Water Tracker", 
    "🧪 Custom Recipes Developer", 
    "📊 Progress & Wearable Sync"
])

# ==================== TAB 1: WEEKLY MEAL PLANNER ====================
with tab1:
    st.write("## Your Clinical Daily Macro & Meal Targets")
    
    # Render Dashboard Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"<div class='metric-box'><strong>Target Calories</strong><br/><span style='font-size: 24px; color: #1e5249; font-weight:bold;'>{int(target_calories)} kcal</span></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='metric-box'><strong>Protein Target</strong><br/><span style='font-size: 24px; color: #d35400; font-weight:bold;'>{int(protein_g)}g</span></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='metric-box'><strong>Carb Target</strong><br/><span style='font-size: 24px; color: #2980b9; font-weight:bold;'>{int(carbs_g)}g</span></div>", unsafe_allow_html=True)
    with m4:
        st.markdown(f"<div class='metric-box'><strong>Fat Target</strong><br/><span style='font-size: 24px; color: #f1c40f; font-weight:bold;'>{int(fats_g)}g</span></div>", unsafe_allow_html=True)
        
    st.write("---")
    
    # Servings Scale Controller
    servings_scale = st.slider("⚖️ Servings Scaler (Multiply portions globally)", 1, 6, 1)
    
    if not st.session_state.weekly_plan:
        st.info("👈 Please initialize your baseline parameters and click 'Generate & Sync New Profile' on the sidebar.")
    else:
        # Render days inside tabs
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_tabs = st.tabs(day_names)
        
        for index, day in enumerate(day_names):
            with day_tabs[index]:
                meals = st.session_state.weekly_plan[day]
                st.write(f"### Meal Plan for {day}")
                
                for category in ["Breakfast", "Lunch", "Dinner", "Snack"]:
                    meal_item = meals[category]
                    col_meal, col_action = st.columns([5, 1])
                    
                    with col_meal:
                        st.markdown(f"""
                        <div class='meal-card'>
                            <span style='color: #7f8c8d; font-size: 12px; font-weight: bold;'>{category.upper()}</span>
                            <h4>{meal_item['name']}</h4>
                            <p style='margin: 0; color: #34495e; font-size:14px;'>
                                🔋 Calories: <strong>{meal_item['calories'] * servings_scale} kcal</strong> | 
                                🍗 Protein: <strong>{meal_item['protein'] * servings_scale}g</strong> | 
                                🍞 Carbs: <strong>{meal_item['carbs'] * servings_scale}g</strong> | 
                                🧈 Fats: <strong>{meal_item['fats'] * servings_scale}g</strong>
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    with col_action:
                        # Dynamic swap action
                        st.write(" ")
                        st.write(" ")
                        if st.button(f"🔄 Swap", key=f"swap_{day}_{category}"):
                            alternatives = get_filtered_meals(category, avoid_tags, [])
                            new_meal = random.choice(alternatives)
                            st.session_state.weekly_plan[day][category] = new_meal
                            st.rerun()

# ==================== TAB 2: GROCERY BUILDER ====================
with tab2:
    st.write("## Dynamic Aisle-by-Aisle Shopping List")
    st.write("This list automatically tracks and aggregates ingredients from your custom weekly meal plan.")
    
    if not st.session_state.weekly_plan:
        st.info("Generate a plan in Tab 1 to unlock your automated grocery list.")
    else:
        # Parse ingredients from meal plans
        categorized_grocery = {}
        for day, day_meals in st.session_state.weekly_plan.items():
            for category, item in day_meals.items():
                aisle = item.get("aisle", "Pantry")
                for ingredient in item["ingredients"]:
                    scaled_ingredient = f"{ingredient} (for {servings_scale}x portion)"
                    if aisle not in categorized_grocery:
                        categorized_grocery[aisle] = set()
                    categorized_grocery[aisle].add(scaled_ingredient)

        # Render lists by aisle
        c1, c2 = st.columns(2)
        half_length = len(categorized_grocery) // 2
        
        for i, (aisle, ingredients) in enumerate(categorized_grocery.items()):
            target_col = c1 if i < half_length else c2
            with target_col:
                st.write(f"### 📦 {aisle} Aisle")
                for item in ingredients:
                    key_id = f"check_{aisle}_{item}"
                    if key_id not in st.session_state.grocery_checklist:
                        st.session_state.grocery_checklist[key_id] = False
                    
                    st.checkbox(item, key=key_id)
        
        st.write("---")
        st.write("### ➕ Manual Grocery Additions")
        col_new_grocery, col_add_btn = st.columns([4, 1])
        with col_new_grocery:
            manual_item = st.text_input("Need to buy extra stuff? Enter item here:", placeholder="e.g. Dish soap, Napkins")
        with col_add_btn:
            st.write(" ")
            if st.button("Add Item", use_container_width=True) and manual_item:
                st.session_state.manual_groceries.append(manual_item)
                st.rerun()
                
        if st.session_state.manual_groceries:
            st.write("#### Custom items:")
            for index, extra_item in enumerate(st.session_state.manual_groceries):
                st.checkbox(extra_item, key=f"manual_{index}")

# ==================== TAB 3: WATER & FOOD LOGGING ====================
with tab3:
    st.write("## Daily Interactive Intake Trackers")
    
    cl_log1, cl_log2 = st.columns(2)
    
    with cl_log1:
        st.write("### 💧 Hydro Tracker")
        st.write("Stay hydrated! Track your progress towards your recommended target (8-12 cups).")
        st.metric("Today's Water Level", f"{st.session_state.water_intake} Cups", "Target: 8 Cups")
        
        col_w1, col_w2, col_w3 = st.columns(3)
        with col_w1:
            if st.button("➕ 1 Cup (250ml)", use_container_width=True):
                st.session_state.water_intake += 1
                st.rerun()
        with col_w2:
            if st.button("➖ 1 Cup", use_container_width=True) and st.session_state.water_intake > 0:
                st.session_state.water_intake -= 1
                st.rerun()
        with col_w3:
            if st.button("🧹 Reset Tracker", use_container_width=True):
                st.session_state.water_intake = 0
                st.rerun()
                
    with cl_log2:
        st.write("### 📸 Integrated Barcode Scanner (Simulated)")
        st.write("Scan physical UPC labels to instantly pull custom nutritional metrics.")
        barcode_input = st.text_input("Simulate Barcode Input (Scan or enter 4-digit code):", placeholder="Try scanning '9901' or '9902'")
        
        if barcode_input:
            if barcode_input == "9901":
                st.success("✅ Barcode Matched: Premium Organic Peanut Butter")
                st.info("Metrics: 190 kcal | 8g Protein | 6g Carbs | 16g Fats")
                if st.button("Log Butter to Tracker"):
                    st.session_state.logged_meals.append({"name": "Organic Peanut Butter", "calories": 190, "protein": 8, "carbs": 6, "fats": 16})
            elif barcode_input == "9902":
                st.success("✅ Barcode Matched: Raw Whey Protein Isolate")
                st.info("Metrics: 120 kcal | 25g Protein | 2g Carbs | 1g Fats")
                if st.button("Log Whey to Tracker"):
                    st.session_state.logged_meals.append({"name": "Whey Protein Isolate", "calories": 120, "protein": 25, "carbs": 2, "fats": 1})
            else:
                st.error("❌ Barcode not found in local sync directory. Try adding a custom recipe instead.")

    st.write("---")
    st.write("### 🧾 Daily Intake Log Summary")
    
    # Food search quick database logging
    search_food = st.selectbox("Search master database to log meals:", [""] + [f["name"] for f in get_master_food_db()])
    if search_food != "":
        match_food = next(f for f in get_master_food_db() if f["name"] == search_food)
        if st.button(f"Log {match_food['name']} into Today's Diary"):
            st.session_state.logged_meals.append(match_food)
            st.success("Logged!")
            st.rerun()

    if st.session_state.logged_meals:
        df_logged = pd.DataFrame(st.session_state.logged_meals)
        st.dataframe(df_logged, use_container_width=True)
        st.write(f"**Total Logged Calories:** {df_logged['calories'].sum()} kcal / {int(target_calories)} kcal limit")
        if st.button("Clear Intake Log"):
            st.session_state.logged_meals = []
            st.rerun()
    else:
        st.info("No dietary entries logged for today yet.")

# ==================== TAB 4: CUSTOM RECIPE CREATOR ====================
with tab4:
    st.write("## 🧪 Create & Save Your Custom Recipes")
    st.write("Design specialized, personal culinary combinations and save them directly into your generator engine database.")
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        recipe_name = st.text_input("Recipe / Meal Name", placeholder="My Signature Protein Shake")
        recipe_cal = st.number_input("Calories (kcal)", 0, 2500, 300)
        recipe_category = st.selectbox("Assign Meal Category", ["Breakfast", "Lunch", "Dinner", "Snack"])
        
    with col_r2:
        recipe_prot = st.number_input("Protein (g)", 0, 200, 25)
        recipe_carbs = st.number_input("Carbs (g)", 0, 500, 30)
        recipe_fats = st.number_input("Fats (g)", 0, 200, 10)
        
    recipe_ingredients = st.text_area("Ingredients list (comma-separated):", placeholder="Whey Protein, Bananas, Spinach, Almond milk")
    
    # Process custom tags
    custom_tags = []
    if recipe_carbs <= 15:
        custom_tags.append("K")
    if "Meat" not in recipe_ingredients and "Chicken" not in recipe_ingredients:
        custom_tags.append("V")
    custom_tags.append("GF")
    custom_tags.append("NF")

    if st.button("💾 Save Recipe to Master Library"):
        if recipe_name and recipe_ingredients:
            new_recipe_item = {
                "id": random.randint(1000, 9999),
                "name": recipe_name,
                "calories": recipe_cal,
                "protein": recipe_prot,
                "carbs": recipe_carbs,
                "fats": recipe_fats,
                "category": recipe_category,
                "tags": custom_tags,
                "ingredients": [i.strip() for i in recipe_ingredients.split(",")],
                "aisle": "Pantry"
            }
            st.session_state.custom_recipes.append(new_recipe_item)
            st.success(f"Custom recipe '{recipe_name}' has been compiled and cataloged!")
        else:
            st.error("Please fill out both the recipe name and ingredients list to compile.")

    if st.session_state.custom_recipes:
        st.write("---")
        st.write("### 📁 Your Saved Custom Recipes")
        st.write(pd.DataFrame(st.session_state.custom_recipes))

# ==================== TAB 5: HEALTH METRIC ANALYTICS ====================
with tab5:
    st.write("## 📉 Historical Metrics & Wearable Integrations")
    
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        st.write("### 🏋️ Weight & Body Metric Log")
        new_wt = st.number_input("Log Weight Entry (kg)", 30.0, 200.0, float(weight), step=0.1)
        if st.button("Commit Metric to Log"):
            new_row = pd.DataFrame([{"Date": datetime.now().strftime("%Y-%m-%d"), "Weight": new_wt}])
            st.session_state.weight_history = pd.concat([st.session_state.weight_history, new_row], ignore_index=True)
            st.success("Biometric coordinate logged!")
            st.rerun()
            
        st.write("#### Recorded Progression History")
        st.line_chart(st.session_state.weight_history.set_index("Date"))
        
    with col_a2:
        st.write("### ⌚ Wearable Sync Center")
        st.write("Synchronize physical activities from Fitbit, Garmin, or Apple Health APIs.")
        
        st.info("API Integrations are configured to default test channels.")
        
        st.metric("Today's Sync Active Burn", f"{st.session_state.steps_synced} Steps", "+185 Active kcal")
        
        if st.button("⚡ Force Remote API Sync Now"):
            st.session_state.steps_synced += random.randint(1500, 4500)
            st.success("API Pull complete: Synced with local mobile background daemon!")
            st.rerun()

        st.markdown("""
        <div style="background-color: #f1f2f6; border-radius: 10px; padding: 15px;">
            <p style="margin: 0; font-size:12px; color: #57606f;"><strong>Connected Wearable Metadata:</strong><br/>
            API Server Address: <code>https://api.fitbit.com/1/user/-/activities/</code><br/>
            Auth State: <code>Token Verified (Active)</code><br/>
            Last Handshake: 2026-07-16 00:00:23</p>
        </div>
        """, unsafe_allow_html=True)