import os
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

try:
    from groq import Groq
except ImportError:
    Groq = None

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


BASE_DIR = Path(__file__).resolve().parent

import gdown

if not (BASE_DIR / "pipeline.pkl").exists():
    gdown.download(
        "https://drive.google.com/file/d/1cSUJBLMu9HA52382odHJEz17nNwo5l37/view?usp=sharing",
        str(BASE_DIR / "pipeline.pkl"),
        quiet=False
    )

if not (BASE_DIR / "carbon_pipeline.pkl").exists():
    gdown.download(
        "https://drive.google.com/file/d/1skRcYsMpvJt2ZJbewzsOxHeezy1lh9ky/view?usp=sharing",
        str(BASE_DIR / "carbon_pipeline.pkl"),
        quiet=False
    )

DATA_PATHS = [BASE_DIR / "Carbon Emission.csv", BASE_DIR / "Carbon_Emission.csv"]
MODEL_PATHS = [BASE_DIR / "pipeline.pkl", BASE_DIR / "carbon_pipeline.pkl"]

IMAGE_LIBRARY = {
}

WEB_TIPS = {
    "transport": {
        "title": "Shift short trips away from solo driving",
        "body": "Walking, cycling, ride-sharing, and public transport are some of the clearest ways to reduce transport emissions in day-to-day life.",
        "source": "IEA: Saving Energy",
        "url": "https://www.iea.org/topics/saving-energy",
    },
    "energy": {
        "title": "Cut home energy waste first",
        "body": "Small actions like improving efficient appliances, lowering heating demand, and tightening home energy habits can reduce both emissions and bills.",
        "source": "EPA: Pollution Prevention Tips for Energy Efficiency",
        "url": "https://www.epa.gov/p2/pollution-prevention-tips-energy-efficiency",
    },
    "waste": {
        "title": "Prevent food waste before it happens",
        "body": "Meal planning, buying only what you will use, and using leftovers reduce landfill methane and the hidden emissions from producing wasted food.",
        "source": "EPA: Preventing Wasted Food At Home",
        "url": "https://www.epa.gov/recycle/reducing-wasted-food-home",
    },
    "baseline": {
        "title": "Track home energy, transport, and waste together",
        "body": "Those three areas are a practical baseline for household footprint reduction and help explain where the biggest gains usually come from.",
        "source": "EPA: Household Carbon Footprint Calculator",
        "url": "https://www.epa.gov/ghgemissions/household-carbon-footprint-calculator",
    },
}


st.set_page_config(
    page_title="AI Carbon Footprint Studio",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Manrope:wght@400;500;600;700&display=swap');

    :root {
        --bg: #071b12;
        --panel: rgba(10, 36, 24, 0.88);
        --panel-strong: rgba(12, 44, 29, 0.96);
        --text: #f3fff7;
        --muted: #b7d7c3;
        --accent: #53c68c;
        --accent-2: #9be7b6;
        --border: rgba(83, 198, 140, 0.18);
        --shadow: 0 20px 60px rgba(0, 0, 0, 0.28);
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(83, 198, 140, 0.18), transparent 24%),
            radial-gradient(circle at top right, rgba(20, 88, 54, 0.30), transparent 24%),
            radial-gradient(circle at 20% 70%, rgba(118, 255, 170, 0.10), transparent 18%),
            linear-gradient(180deg, #06140d 0%, #0b2418 100%);
        color: var(--text);
        font-family: 'Manrope', sans-serif;
    }

    h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--text);
        letter-spacing: -0.02em;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #041109 0%, #0d2e1d 55%, #17452d 100%);
    }

    [data-testid="stSidebar"] * {
        color: #f4fff7;
    }

    .hero-card, .glass-card, .tip-card {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 24px;
        box-shadow: var(--shadow);
        backdrop-filter: blur(14px);
    }

    .hero-card {
        padding: 1.6rem 1.6rem 1.2rem 1.6rem;
    }

    .glass-card {
        padding: 1.1rem 1.2rem;
        min-height: 148px;
    }

    .tip-card {
        padding: 1rem 1.1rem;
        margin-bottom: 0.8rem;
    }

    .eyebrow {
        display: inline-block;
        padding: 0.3rem 0.75rem;
        border-radius: 999px;
        background: rgba(83, 198, 140, 0.14);
        color: var(--accent);
        font-size: 0.86rem;
        font-weight: 700;
        margin-bottom: 0.9rem;
    }

    .hero-copy {
        font-size: 1.02rem;
        color: var(--muted);
        line-height: 1.75;
    }

    .metric-label {
        font-size: 0.88rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #d6f5e3;
        margin-bottom: 0.35rem;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff;
    }

    .metric-subtext {
        color: #dcefe3;
        font-size: 0.92rem;
    }

    .ai-box {
        background: rgba(8, 29, 19, 0.96);
        border: 1px solid rgba(47, 158, 114, 0.24);
        border-radius: 22px;
        padding: 1rem 1.1rem;
        color: #f3fff7;
        box-shadow: var(--shadow);
    }

    .info-banner {
        background: rgba(13, 46, 29, 0.95);
        border: 1px solid rgba(83, 198, 140, 0.28);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        margin: 1rem 0 1.2rem 0;
        color: #ffffff;
        font-size: 1rem;
        font-weight: 600;
    }

    .status-pill {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 999px;
        font-weight: 700;
        background: rgba(83, 198, 140, 0.16);
        color: #d8ffe7;
    }

    .stButton > button {
        width: 100%;
        border: none;
        border-radius: 16px;
        background: linear-gradient(135deg, #2f9e72, #53c68c);
        color: #041109;
        font-weight: 700;
        padding: 0.8rem 1rem;
        box-shadow: 0 12px 30px rgba(47, 158, 114, 0.24);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(11, 36, 24, 0.88);
        border-radius: 999px;
        padding: 0.35rem 1rem;
        height: 44px;
        color: #dff8e8;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(83, 198, 140, 0.18);
        color: var(--accent) !important;
    }

    div[data-testid="stMetric"] {
        background: var(--panel-strong);
        border: 1px solid var(--border);
        padding: 0.9rem 1rem;
        border-radius: 20px;
    }

    .stMarkdown, .stText, .stCaption, p, label, div {
        color: var(--text);
    }
</style>
""",
    unsafe_allow_html=True,
)


if load_dotenv is not None:
    load_dotenv(BASE_DIR / ".env.local", override=False)


@st.cache_resource
def load_model():
    for path in MODEL_PATHS:
        if path.exists():
            return joblib.load(path)
    return None


@st.cache_data
def load_data():
    for path in DATA_PATHS:
        if path.exists():
            return pd.read_csv(path)
    return None


def get_image_path(name: str) -> Path | None:
    path = IMAGE_LIBRARY.get(name)
    return path if path and path.exists() else None


def format_period_projection(monthly_value: float):
    daily = monthly_value / 30
    weekly = daily * 7
    yearly = monthly_value * 12
    return {
        "1 Day": daily,
        "1 Week": weekly,
        "1 Month": monthly_value,
        "1 Year": yearly,
    }


def get_options(dataframe: pd.DataFrame, column: str):
    if dataframe is None or column not in dataframe.columns:
        return []
    return sorted(dataframe[column].dropna().astype(str).unique().tolist())


def match_value(value: str, dataframe: pd.DataFrame, column: str):
    options = get_options(dataframe, column)
    if not options:
        return value
    candidate = value.strip().lower()
    if not candidate:
        return options[0]
    for item in options:
        if candidate == item.lower():
            return item
    for item in options:
        if candidate in item.lower():
            return item
    return options[0]


def build_user_frame(dataframe: pd.DataFrame, pipeline_model, payload: dict) -> pd.DataFrame:
    user_input_df = pd.DataFrame([payload])
    if hasattr(pipeline_model, "feature_names_in_"):
        user_input_df = user_input_df[pipeline_model.feature_names_in_]
    return user_input_df


def get_status(yearly_emission: float):
    if yearly_emission < 2000:
        return "Eco-Friendly", "Low carbon lifestyle", "#22c55e"
    if yearly_emission < 5000:
        return "Moderate", "Some reduction opportunities", "#ff9f43"
    return "High Impact", "Strong action recommended", "#ff6b6b"


def estimate_breakdown(monthly_emission: float, state: dict):
    weighted_inputs = {
        "Transport": max(state["monthly_distance"], 1) * 0.35,
        "Food": max(state["monthly_grocery"], 1) * 0.20,
        "Digital + Home": max(state["internet"] + state["tv"], 1) * 0.25,
        "Shopping": max(state["clothes"], 1) * 0.12,
        "Waste": max(state["waste_count"], 1) * 0.08,
    }
    total = sum(weighted_inputs.values())
    return {key: monthly_emission * (value / total) for key, value in weighted_inputs.items()}


def build_recommendations(state: dict):
    tips = []
    if state["monthly_distance"] > 500:
        tip = WEB_TIPS["transport"]
        tips.append((tip["title"], f"{tip['body']} Source: {tip['source']}"))
    if state["diet"].lower() in {"meat", "omnivore", "pescatarian"}:
        tip = WEB_TIPS["waste"]
        tips.append(("Plan food more carefully", f"{tip['body']} Source: {tip['source']}"))
    if state["internet"] + state["tv"] > 10:
        tip = WEB_TIPS["energy"]
        tips.append(("Reduce unnecessary device energy use", f"{tip['body']} Source: {tip['source']}"))
    if state["energy_eff"].lower() in {"no", "low"}:
        tip = WEB_TIPS["energy"]
        tips.append((tip["title"], f"{tip['body']} Source: {tip['source']}"))
    if state["waste_count"] > 4:
        tip = WEB_TIPS["waste"]
        tips.append((tip["title"], f"{tip['body']} Source: {tip['source']}"))
    if state["clothes"] > 4:
        tip = WEB_TIPS["baseline"]
        tips.append(("Focus on the biggest lifestyle drivers", f"{tip['body']} Source: {tip['source']}"))
    if not tips:
        tip = WEB_TIPS["baseline"]
        tips.append((tip["title"], f"{tip['body']} Source: {tip['source']}"))
    return tips


def scenario_projection(current_monthly: float, travel_cut: int, screen_cut: int, shopping_cut: int):
    reduction_ratio = (travel_cut * 0.0035) + (screen_cut * 0.012) + (shopping_cut * 0.018)
    reduction_ratio = min(max(reduction_ratio, 0), 0.55)
    improved_monthly = current_monthly * (1 - reduction_ratio)
    savings = current_monthly - improved_monthly
    return improved_monthly, savings, reduction_ratio


def generate_ai_response(api_key: str, monthly: float, yearly: float, state: dict, simulation: dict):
    if Groq is None:
        return None, "The `groq` package is not installed yet. Add it from `requirements.txt` and restart the app."

    try:
        client = Groq(api_key=api_key)
        prompt = f"""
You are a sustainability coach for a carbon footprint prediction app.
Give a friendly, practical response in 3 short sections:
1. Lifestyle diagnosis
2. Top 3 actions
3. One motivational closing line

User profile:
- Monthly emission: {monthly:.2f} kg CO2
- Yearly emission: {yearly:.2f} kg CO2
- Transport monthly distance: {state['monthly_distance']:.1f} km
- Grocery spend monthly: {state['monthly_grocery']:.1f}
- Internet hours daily: {state['internet']:.1f}
- TV/PC hours daily: {state['tv']:.1f}
- New clothes monthly: {state['clothes']:.1f}
- Waste bags weekly: {state['waste_count']:.1f}
- Diet: {state['diet']}
- Energy efficiency: {state['energy_eff']}
- Scenario monthly emission after improvements: {simulation['projected_monthly']:.2f} kg CO2
- Scenario monthly savings: {simulation['monthly_savings']:.2f} kg CO2
"""
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.5,
            max_tokens=500,
            messages=[
                {"role": "system", "content": "Be concise, actionable, and easy for a student project demo audience."},
                {"role": "user", "content": prompt},
            ],
        )
        return completion.choices[0].message.content, None
    except Exception as exc:
        return None, str(exc)


def maybe_generate_ai_suggestions():
    groq_api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not groq_api_key or st.session_state.prediction is None:
        return
    if st.session_state.ai_response or st.session_state.ai_error:
        return

    monthly = st.session_state.prediction
    yearly = monthly * 12
    projected_monthly, monthly_savings, _ = scenario_projection(monthly, 15, 10, 10)
    response, error = generate_ai_response(
        groq_api_key,
        monthly,
        yearly,
        {
            "monthly_distance": st.session_state.monthly_distance,
            "monthly_grocery": st.session_state.monthly_grocery,
            "internet": st.session_state.internet,
            "tv": st.session_state.tv,
            "clothes": st.session_state.clothes,
            "waste_count": st.session_state.waste_count,
            "diet": st.session_state.diet,
            "energy_eff": st.session_state.energy_eff,
        },
        {
            "projected_monthly": projected_monthly,
            "monthly_savings": monthly_savings,
        },
    )
    st.session_state.ai_response = response
    st.session_state.ai_error = error


pipeline = load_model()
df = load_data()

if pipeline is None or df is None:
    st.error("Model or data file is missing. Keep `pipeline.pkl` or `carbon_pipeline.pkl` and `Carbon Emission.csv` in this folder.")
    st.stop()


default_state = {
    "prediction": None,
    "monthly_distance": 0.0,
    "internet": 0.0,
    "tv": 0.0,
    "monthly_grocery": 0.0,
    "clothes": 0.0,
    "waste_count": 0.0,
    "diet": "",
    "energy_eff": "",
    "ai_response": None,
    "ai_error": None,
}
for key, value in default_state.items():
    st.session_state.setdefault(key, value)


st.markdown(
    """
<div class="hero-card">
    <div class="eyebrow">AI-powered sustainability studio</div>
    <h1 style="margin-bottom:0.5rem;">Sustainable Carbon Footprint Calculator</h1>
    <p class="hero-copy">
        Predict your lifestyle emissions, compare yourself with the dataset, explore what-if reductions,
        and generate a personalized action plan using Groq-powered AI.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.title("Lifestyle Input")
    st.caption("Fill in your daily habits, then run prediction and AI coaching from `.env.local`.")

    with st.form("lifestyle_form"):
        with st.expander("Personal profile", expanded=True):
            body = st.selectbox("Body Type", get_options(df, "Body Type"))
            sex = st.selectbox("Sex", get_options(df, "Sex"))
            diet = st.selectbox("Diet", get_options(df, "Diet"))
            social = st.selectbox("Social Activity", get_options(df, "Social Activity"))

        with st.expander("Home and consumption", expanded=True):
            grocery = st.number_input("Daily Grocery Spending", min_value=0.0, max_value=2000.0, value=250.0, step=10.0)
            clothes = st.number_input("New Clothes per Month", min_value=0.0, max_value=30.0, value=2.0, step=1.0)
            shower = st.selectbox("How Often Shower", get_options(df, "How Often Shower"))
            heating = st.selectbox("Heating Energy Source", get_options(df, "Heating Energy Source"))
            cooking_input = st.text_input("Cooking With", value="gas")

        with st.expander("Transport", expanded=True):
            transport = st.selectbox("Transport Mode", get_options(df, "Transport"))
            vehicle_type = st.selectbox("Vehicle Type", get_options(df, "Vehicle Type"))
            distance = st.slider("Daily Travel Distance (km)", min_value=0.0, max_value=250.0, value=12.0, step=1.0)
            air = st.selectbox("Air Travel Frequency", get_options(df, "Frequency of Traveling by Air"))

        with st.expander("Digital and waste", expanded=True):
            energy_eff = st.selectbox("Energy Efficient Appliances", get_options(df, "Energy efficiency"))
            internet = st.slider("Internet Usage (hrs/day)", min_value=0.0, max_value=24.0, value=5.0, step=0.5)
            tv = st.slider("TV / PC Usage (hrs/day)", min_value=0.0, max_value=24.0, value=3.0, step=0.5)
            waste_size = st.selectbox("Waste Bag Size", get_options(df, "Waste Bag Size"))
            waste_count = st.number_input("Waste Bags Weekly", min_value=0.0, max_value=20.0, value=2.0, step=1.0)
            recycling_input = st.text_input("Recycling", value="paper")

        submitted = st.form_submit_button("Predict My Footprint")


if submitted:
    recycling = match_value(recycling_input, df, "Recycling")
    cooking = match_value(cooking_input, df, "Cooking_With")
    monthly_distance = distance * 30
    monthly_grocery = grocery * 30

    user_input = {
        "Body Type": body,
        "Sex": sex,
        "Diet": diet,
        "How Often Shower": shower,
        "Heating Energy Source": heating,
        "Transport": transport,
        "Vehicle Type": vehicle_type,
        "Social Activity": social,
        "Monthly Grocery Bill": monthly_grocery,
        "Frequency of Traveling by Air": air,
        "Vehicle Monthly Distance Km": monthly_distance,
        "Waste Bag Size": waste_size,
        "Waste Bag Weekly Count": waste_count,
        "How Long TV PC Daily Hour": tv,
        "How Many New Clothes Monthly": clothes,
        "How Long Internet Daily Hour": internet,
        "Energy efficiency": energy_eff,
        "Recycling": recycling,
        "Cooking_With": cooking,
    }

    try:
        user_df = build_user_frame(df, pipeline, user_input)
        prediction = float(pipeline.predict(user_df)[0])
        st.session_state.prediction = prediction
        st.session_state.monthly_distance = monthly_distance
        st.session_state.internet = internet
        st.session_state.tv = tv
        st.session_state.monthly_grocery = monthly_grocery
        st.session_state.clothes = clothes
        st.session_state.waste_count = waste_count
        st.session_state.diet = diet
        st.session_state.energy_eff = energy_eff
        st.session_state.ai_response = None
        st.session_state.ai_error = None
        maybe_generate_ai_suggestions()
    except Exception as exc:
        st.error(f"Prediction failed. Please verify the model features and inputs. Details: {exc}")


if st.session_state.prediction is None:
    st.markdown(
        """
<div class="info-banner">
    Enter your details in the sidebar and click <strong>Predict My Footprint</strong> to see your emission analysis,
    time-scale graph, and web-grounded sustainability suggestions.
</div>
""",
        unsafe_allow_html=True,
    )
else:
    monthly = st.session_state.prediction
    yearly = monthly * 12
    status, status_text, status_color = get_status(yearly)
    period_projection = format_period_projection(monthly)
    breakdown = estimate_breakdown(
        monthly,
        {
            "monthly_distance": st.session_state.monthly_distance,
            "monthly_grocery": st.session_state.monthly_grocery,
            "internet": st.session_state.internet,
            "tv": st.session_state.tv,
            "clothes": st.session_state.clothes,
            "waste_count": st.session_state.waste_count,
        },
    )

    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Analytics", "Reduction Lab", "AI Coach"])

    with tab1:
        top_cols = st.columns(4)
        cards = [
            ("Estimated Monthly CO2", f"{monthly:.1f} kg", "Predicted from your current lifestyle pattern."),
            ("Estimated Yearly CO2", f"{yearly / 1000:.2f} tons", "Useful for sustainability benchmarking and project demos."),
            ("Lifestyle Status", status, status_text),
            ("Tree Offset Need", f"{yearly / 21:.0f} trees", "Approximate number of trees needed yearly to offset this amount."),
        ]
        for idx, (label, value, subtext) in enumerate(cards):
            with top_cols[idx]:
                st.markdown(
                    f"""
<div class="glass-card">
    <div class="metric-label">{label}</div>
    <div class="metric-value" style="color:{status_color if label == 'Lifestyle Status' else 'var(--text)'};">{value}</div>
    <div class="metric-subtext">{subtext}</div>
</div>
""",
                    unsafe_allow_html=True,
                )

        left, right = st.columns([1.25, 1], gap="large")
        with left:
            fig_breakdown = px.pie(
                names=list(breakdown.keys()),
                values=list(breakdown.values()),
                hole=0.6,
                color=list(breakdown.keys()),
                color_discrete_sequence=["#ff6b6b", "#ff9f43", "#22c55e", "#4d96ff", "#845ec2"],
            )
            fig_breakdown.update_layout(
                title="Estimated Monthly Emission Mix",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                legend_title_text="Category",
                font=dict(size=16, color="#ffffff"),
                title_font=dict(size=22, color="#ffffff"),
                legend=dict(font=dict(size=14, color="#ffffff")),
                margin=dict(t=70, b=20, l=20, r=20),
            )
            fig_breakdown.update_traces(
                textposition="inside",
                textfont_size=14,
                textfont_color="#ffffff",
                hovertemplate="%{label}: %{value:.1f} kg<extra></extra>",
            )
            st.plotly_chart(fig_breakdown, use_container_width=True)
        with right:
            compare_mean = float(df["CarbonEmission"].mean()) if "CarbonEmission" in df.columns else 0
            percentile = float((df["CarbonEmission"] <= monthly).mean() * 100) if "CarbonEmission" in df.columns else 0
            st.markdown(
                f"""
<div class="glass-card">
    <div class="metric-label">Dataset comparison</div>
    <div class="metric-value">{percentile:.0f}th percentile</div>
    <div class="metric-subtext">Your monthly emission is compared against the people represented in the training dataset.</div>
    <br>
    <div class="status-pill">Dataset average: {compare_mean:.1f} kg/month</div>
</div>
""",
                unsafe_allow_html=True,
            )
            insight_img = get_image_path("category")
            if insight_img:
                st.image(str(insight_img), use_container_width=True)

    with tab2:
        chart_left, chart_right = st.columns([1.3, 1], gap="large")
        with chart_left:
            fig_timescale = px.line(
                x=list(period_projection.keys()),
                y=list(period_projection.values()),
                markers=True,
                labels={"x": "Prediction period", "y": "Estimated CO2 (kg)"},
                title="Prediction Across Time Scales",
                color_discrete_sequence=["#3a86ff"],
            )
            fig_timescale.update_traces(line=dict(width=4), marker=dict(size=12), hovertemplate="%{x}: %{y:.2f} kg<extra></extra>")
            fig_timescale.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(size=16, color="#ffffff"),
                title_font=dict(size=22, color="#ffffff"),
                xaxis=dict(title_font=dict(size=16, color="#ffffff"), tickfont=dict(size=14, color="#ffffff"), showgrid=False, color="#ffffff"),
                yaxis=dict(title_font=dict(size=16, color="#ffffff"), tickfont=dict(size=14, color="#ffffff"), gridcolor="rgba(255, 255, 255, 0.12)", color="#ffffff"),
                margin=dict(t=70, b=40, l=20, r=20),
            )
            st.plotly_chart(fig_timescale, use_container_width=True)
        with chart_right:
            fig_hist = px.histogram(
                df,
                x="CarbonEmission",
                nbins=40,
                title="Population Distribution vs Your Result",
                color_discrete_sequence=["#82c7ff"],
            )
            fig_hist.add_vline(x=monthly, line_width=3, line_dash="dash", line_color="#ff6b6b")
            fig_hist.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis_title="Carbon Emission (kg/month)",
                yaxis_title="Count",
                font=dict(size=16, color="#ffffff"),
                title_font=dict(size=22, color="#ffffff"),
                xaxis=dict(title_font=dict(size=16, color="#ffffff"), tickfont=dict(size=13, color="#ffffff"), color="#ffffff"),
                yaxis=dict(title_font=dict(size=16, color="#ffffff"), tickfont=dict(size=13, color="#ffffff"), color="#ffffff"),
                margin=dict(t=70, b=40, l=20, r=20),
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        fig_category_line = px.line(
            x=list(breakdown.keys()),
            y=list(breakdown.values()),
            markers=True,
            labels={"x": "Category", "y": "Estimated monthly CO2 (kg)"},
            title="Category-Wise Emission Trend",
            color_discrete_sequence=["#ff6b6b"],
        )
        fig_category_line.update_traces(line=dict(width=4), marker=dict(size=12), hovertemplate="%{x}: %{y:.1f} kg<extra></extra>")
        fig_category_line.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(size=16, color="#ffffff"),
            title_font=dict(size=22, color="#ffffff"),
            xaxis=dict(title_font=dict(size=16, color="#ffffff"), tickfont=dict(size=13, color="#ffffff"), color="#ffffff"),
            yaxis=dict(title_font=dict(size=16, color="#ffffff"), tickfont=dict(size=13, color="#ffffff"), gridcolor="rgba(255, 255, 255, 0.12)", color="#ffffff"),
            margin=dict(t=70, b=40, l=20, r=20),
        )
        st.plotly_chart(fig_category_line, use_container_width=True)

    with tab3:
        st.write("Use the sliders below to model a practical carbon reduction plan.")
        travel_cut = st.slider("Reduce travel distance by (%)", 0, 60, 15, 5)
        screen_cut = st.slider("Reduce digital/screen hours by (%)", 0, 60, 10, 5)
        shopping_cut = st.slider("Reduce shopping/clothing by (%)", 0, 60, 10, 5)

        projected_monthly, monthly_savings, reduction_ratio = scenario_projection(
            monthly, travel_cut, screen_cut, shopping_cut
        )
        projected_yearly = projected_monthly * 12

        sim_cols = st.columns(3)
        sim_cols[0].metric("Projected Monthly CO2", f"{projected_monthly:.1f} kg", delta=f"-{monthly_savings:.1f} kg")
        sim_cols[1].metric("Projected Yearly CO2", f"{projected_yearly / 1000:.2f} tons", delta=f"-{monthly_savings * 12 / 1000:.2f} tons")
        sim_cols[2].metric("Estimated Reduction", f"{reduction_ratio * 100:.0f}%")

        waterfall = go.Figure(
            go.Waterfall(
                name="Reduction",
                orientation="v",
                measure=["absolute", "relative", "relative", "relative", "total"],
                x=["Current", "Travel", "Digital", "Shopping", "Projected"],
                y=[monthly, -(monthly * travel_cut * 0.0035), -(monthly * screen_cut * 0.012), -(monthly * shopping_cut * 0.018), 0],
                connector={"line": {"color": "rgba(23,49,38,0.25)"}},
            )
        )
        waterfall.update_layout(
            title="Scenario Impact Waterfall",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(size=16, color="#ffffff"),
            title_font=dict(size=22, color="#ffffff"),
            xaxis=dict(title_font=dict(size=16, color="#ffffff"), tickfont=dict(size=13, color="#ffffff"), color="#ffffff"),
            yaxis=dict(title_font=dict(size=16, color="#ffffff"), tickfont=dict(size=13, color="#ffffff"), color="#ffffff"),
        )
        st.plotly_chart(waterfall, use_container_width=True)

        tips = build_recommendations(
            {
                "monthly_distance": st.session_state.monthly_distance,
                "internet": st.session_state.internet,
                "tv": st.session_state.tv,
                "monthly_grocery": st.session_state.monthly_grocery,
                "clothes": st.session_state.clothes,
                "waste_count": st.session_state.waste_count,
                "diet": st.session_state.diet,
                "energy_eff": st.session_state.energy_eff,
            }
        )
        for title, body_text in tips:
            st.markdown(f"<div class='tip-card'><strong>{title}</strong><br>{body_text}</div>", unsafe_allow_html=True)

        st.markdown("### Web-Based Guidance")
        st.markdown(
            f"- [IEA: Saving Energy]({WEB_TIPS['transport']['url']})\n"
            f"- [EPA: Preventing Wasted Food At Home]({WEB_TIPS['waste']['url']})\n"
            f"- [EPA: Household Carbon Footprint Calculator]({WEB_TIPS['baseline']['url']})\n"
            f"- [EPA: Pollution Prevention Tips for Energy Efficiency]({WEB_TIPS['energy']['url']})"
        )

        if st.session_state.ai_response:
            st.markdown("### AI-Generated Definite Suggestions")
            st.markdown(f"<div class='ai-box'>{st.session_state.ai_response}</div>", unsafe_allow_html=True)
        elif st.session_state.ai_error:
            st.warning(f"AI suggestion issue: {st.session_state.ai_error}")
        else:
            st.info("AI suggestions will appear here automatically after prediction if `GROQ_API_KEY` is available in `.env.local`.")

    with tab4:
        st.write("Generate a personalized sustainability explanation and action plan using the Groq API.")
        groq_api_key = os.getenv("GROQ_API_KEY", "").strip()
        st.caption("Groq status: " + ("configured" if groq_api_key else "missing from .env.local"))
        simulation_context = {
            "projected_monthly": projected_monthly if "projected_monthly" in locals() else monthly,
            "monthly_savings": monthly_savings if "monthly_savings" in locals() else 0,
        }

        if st.button("Generate AI Sustainability Coach"):
            if not groq_api_key:
                st.warning("Add `GROQ_API_KEY=your_key_here` to `.env.local`, then restart the Streamlit app.")
            else:
                with st.spinner("Contacting Groq and preparing your sustainability advice..."):
                    response, error = generate_ai_response(
                        groq_api_key,
                        monthly,
                        yearly,
                        {
                            "monthly_distance": st.session_state.monthly_distance,
                            "monthly_grocery": st.session_state.monthly_grocery,
                            "internet": st.session_state.internet,
                            "tv": st.session_state.tv,
                            "clothes": st.session_state.clothes,
                            "waste_count": st.session_state.waste_count,
                            "diet": st.session_state.diet,
                            "energy_eff": st.session_state.energy_eff,
                        },
                        simulation_context,
                    )
                    st.session_state.ai_response = response
                    st.session_state.ai_error = error

        if st.session_state.ai_error:
            st.error(f"AI coach error: {st.session_state.ai_error}")

        if st.session_state.ai_response:
            st.markdown("### Personalized AI Coach Output")
            st.markdown(st.session_state.ai_response)
        else:
            st.info("Your AI summary will appear here after you add a key and click the button.")
