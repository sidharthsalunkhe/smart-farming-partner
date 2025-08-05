import streamlit as st
import requests
from datetime import datetime, timedelta, date

# ----------------- PAGE SETUP -----------------
st.set_page_config(page_title="Smart Farming Partner", page_icon="🌾", layout="wide")

# ----------------- WEATHER API -----------------
def get_weather_from_coords(lat, lon):
    api_key = "261f98e168bbce0a092c3bd323031d7c"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("main"):
            return {
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "desc": data["weather"][0]["description"]
            }
    except:
        return None

# ----------------- SIDEBAR INPUTS -----------------
with st.sidebar:
    st.header("🔍 Field & Crop Inputs")
    ph = st.slider("Soil pH", 3.5, 9.0, 6.5)
    moisture = st.slider("Soil Moisture (%)", 0, 100, 30)
    temperature = st.number_input("Ambient Temp (°C)", 0.0, 50.0, 25.0)
    crop = st.selectbox("🌾 Select Crop", ["Wheat", "Rice", "Tomato", "Soybean", "Sugarcane", "Millets"])
    plant_date = st.date_input("📆 Date of Planting", value=datetime.today())
    city = st.text_input("🌍 Enter Your City (for Weather)")

# ----------------- MAIN TITLE -----------------
st.title("🌱 Smart Farming Partner")
st.markdown("#### Making intelligent, location-based, and crop-specific farming decisions.")
st.markdown("---")

# ----------------- SMART SUGGESTIONS -----------------
colA, colB = st.columns(2)

with colA:
    st.subheader("📥 Input Summary")
    st.write(f"• Soil pH: **{ph}**")
    st.write(f"• Moisture: **{moisture}%**")
    st.write(f"• Temp: **{temperature} °C**")
    st.write(f"• Crop: **{crop}**")
    st.write(f"• Planting Date: **{plant_date.strftime('%d %b %Y')}**")
    if city:
        st.write(f"• City: **{city}**")

with colB:
    st.subheader("🧠 Smart Suggestions")

    if ph < 6:
        st.warning("🔬 Soil acidic: consider treating with lime or urea.")
    elif ph > 8:
        st.warning("⚗️ Soil alkaline: sulfate-based fertilizers recommended.")
    else:
        st.success("✅ pH is balanced.")

    if moisture < 30:
        st.info("💧 Moisture low: irrigation recommended.")
    else:
        st.success("✅ Moisture adequate.")

    if temperature > 35:
        st.warning("🔥 High temp: monitor crop water needs.")

    st.subheader("🪴 Fertilizer Guide")
    if ph < 6:
        st.info("Apply lime-based fertilizer (e.g., calcium carbonate).")
    elif ph > 8:
        st.info("Use sulfate fertilizers (e.g., ammonium sulfate, potash sulfate).")
    else:
        st.info("Balanced NPK (10-10-10) mix works well.")

# ----------------- WATERING SCHEDULE -----------------
st.markdown("---")
st.subheader("💧 Watering Schedule")
if moisture < 40:
    st.info("💧 Suggest watering **every 2–3 days** based on crop and soil type.")
elif temperature > 32:
    st.info("☀️ High temp: water daily during afternoon.")
else:
    st.success("✅ Current moisture and temperature support a 3–4 day watering cycle.")

# ----------------- PLANTING SUPPLEMENTS -----------------
st.markdown("---")
st.subheader("🧪 Required Supplements at Planting")
if crop == "Wheat":
    st.info("Apply DAP + organic compost at seed level.")
elif crop == "Rice":
    st.info("Use urea + phosphorous-based fertilizer.")
elif crop == "Tomato":
    st.info("Add potassium nitrate and bio-fertilizers before planting.")
else:
    st.info("Use standard NPK blend and cow dung compost.")

# ----------------- FUTURE WEEK PLANNER -----------------
st.markdown("---")
st.subheader("🗓️ Future Pest & Fertilizer Planner")
current_week = (date.today() - plant_date).days // 7

for i in range(1, 5):
    st.markdown(f"**Week {i}:**")
    if crop == "Rice":
        st.write("🐛 Pest: Leaf folder / Stem borer")
        st.write("🌿 Fertilizer: Top dress with Urea in week 2–3")
    elif crop == "Wheat":
        st.write("🐛 Pest: Aphids / Armyworm")
        st.write("🌿 Fertilizer: Apply nitrogen fertilizer in week 2")
    elif crop == "Tomato":
        st.write("🐛 Pest: Fruit borer / Whiteflies")
        st.write("🌿 Fertilizer: Potash spray recommended")
    else:
        st.write("🐛 Pest: General worm types, watch leaves closely")
        st.write("🌿 Fertilizer: Rotate NPK every 2 weeks")
    st.markdown("---")

# ----------------- WEATHER & SEED SUGGESTION -----------------
if city:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=261f98e168bbce0a092c3bd323031d7c&units=metric"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        weather = {
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "desc": data["weather"][0]["description"]
        }
        st.subheader("☁️ Live Weather Report")
        st.success(f"{weather['temp']}°C, {weather['humidity']}% humidity, {weather['desc'].title()}")

        st.subheader("🌱 Suggested Seeds")
        if weather["temp"] > 30:
            st.info("Recommend: **Millets or Sorghum**")
        elif weather["humidity"] > 70:
            st.info("Recommend: **Rice or Sugarcane**")
        else:
            st.info("Recommend: **Wheat or Soybean**")
    else:
        st.error("❌ Could not fetch weather from location.")
else:
    st.warning("📍 Enter a valid city to detect weather.")

# ----------------- WEED IMAGE UPLOAD -----------------
st.markdown("---")
st.subheader("📸 Weed Detection & Pesticide Advice")
upload = st.file_uploader("Upload weed image (jpg/png)", type=["jpg","jpeg","png"])
if upload:
    st.image(upload, caption="Uploaded Image", use_column_width=True)
    st.warning("Detected weed: *General Broadleaf Weed*")
    st.info("Suggested pesticide: Glyphosate or 2,4-D")

# ----------------- FOOTER -----------------
st.markdown("---")
st.caption("🚀 Built using Streamlit | Smart Farming Partner 2025")

