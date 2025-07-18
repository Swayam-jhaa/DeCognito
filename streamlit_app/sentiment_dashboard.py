import streamlit as st
import pandas as pd
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.express as px

# --- CONFIG ---
CSV_PATH = r"C:\Users\Swaya\Downloads\Faltu\hate_speech_posts_1_year.csv"  # Best for Windows
TEXT_COLS = ["content", "caption"]  # Try both for Twitter/Instagram/LinkedIn
TIME_COLS = ["date", "timestamp"]   # Try both for compatibility

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv(CSV_PATH)
    # Find the first available text and time columns
    text_col = next((col for col in TEXT_COLS if col in df.columns), None)
    time_col = next((col for col in TIME_COLS if col in df.columns), None)
    if not text_col or not time_col:
        st.error("CSV must have a text and a timestamp/date column.")
        st.stop()
    df = df[df[text_col].notnull() & (df[text_col] != "")]
    df["text"] = df[text_col]
    df["timestamp"] = pd.to_datetime(df[time_col], errors="coerce")
    df = df.dropna(subset=["timestamp"])
    return df

# --- SENTIMENT ANALYSIS ---
@st.cache_data
def analyze_sentiment(df):
    analyzer = SentimentIntensityAnalyzer()
    sentiments = []
    scores = []
    for text in df["text"]:
        vs = analyzer.polarity_scores(str(text))
        score = vs["compound"]
        scores.append(score)
        if score >= 0.05:
            sentiments.append("Positive")
        elif score <= -0.05:
            sentiments.append("Negative")
        else:
            sentiments.append("Neutral")
    df["sentiment"] = sentiments
    df["sentiment_score"] = scores
    return df

# --- MAIN APP ---
st.set_page_config(page_title="OSINT Sentiment Timeline", layout="wide")
st.title("📊 OSINT Sentiment Timeline Visualization")

with st.sidebar:
    st.header("Controls")
    reload = st.button("🔄 Reload Data")

# Load and process data
if "df" not in st.session_state or reload:
    df = load_data()
    df = analyze_sentiment(df)
    st.session_state["df"] = df
else:
    df = st.session_state["df"]

# --- TIMELINE AGGREGATION ---
granularity = st.selectbox("Timeline Granularity", ["Day", "Hour"], index=0)
if granularity == "Day":
    df["time_group"] = df["timestamp"].dt.date
else:
    df["time_group"] = df["timestamp"].dt.floor("H")

timeline = df.groupby(["time_group", "sentiment"]).size().reset_index(name="count")
timeline_pivot = timeline.pivot(index="time_group", columns="sentiment", values="count").fillna(0)

# Ensure all sentiment columns exist for plotting
for col in ["Positive", "Neutral", "Negative"]:
    if col not in timeline_pivot.columns:
        timeline_pivot[col] = 0
timeline_pivot = timeline_pivot[["Positive", "Neutral", "Negative"]]

# --- LAYOUT ---
tab1, tab2, tab3 = st.tabs(["📈 Timeline", "🥧 Sentiment Breakdown", "🗃️ Data Table"])

with tab1:
    st.subheader("Sentiment Over Time")
    fig = px.line(
        timeline_pivot,
        x=timeline_pivot.index,
        y=["Positive", "Neutral", "Negative"],
        labels={"value": "Count", "time_group": "Time"},
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Total Sentiment Breakdown")
    pie_data = df["sentiment"].value_counts().reset_index()
    pie_data.columns = ["sentiment", "count"]
    fig2 = px.pie(pie_data, names="sentiment", values="count", color="sentiment",
                  color_discrete_map={"Positive":"green", "Neutral":"gray", "Negative":"red"})
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("Sentiment-Tagged Posts")
    # Only show columns that exist in the dataframe
    display_cols = [col for col in ["platform", "username", "timestamp", "text", "sentiment", "sentiment_score", "url"] if col in df.columns]
    st.dataframe(
        df[display_cols].sort_values("timestamp", ascending=False),
        use_container_width=True,
        hide_index=True
    )

st.caption("Data auto-refreshes on reload. Powered by VADER & Streamlit. OSINT-ready.")