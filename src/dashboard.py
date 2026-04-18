import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import ast

# ตั้งค่า Dashboard
st.set_page_config(
    page_title="News Analysis Dashboard",
    page_icon="📰",
    layout="wide"
)

# โหลดข้อมูล
@st.cache_data
def load_data():
    df = pd.read_csv("D:/Data science/DataTest/ai_news_project/data/bbc_final.csv")
    # แปลงคอลัมน์ persons จาก string เป็น list
    df["persons"] = df["persons"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else []
    )
    return df

df = load_data()

# ==================== Header ====================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(" บทความทั้งหมด", f"{len(df)} บทความ")
with col2:
    pos = len(df[df["sentiment"] == "Positive"])
    st.metric(" Positive", pos)
with col3:
    neg = len(df[df["sentiment"] == "Negative"])
    st.metric(" Negative", neg)
with col4:
    neu = len(df[df["sentiment"] == "Neutral"])
    st.metric(" Neutral", neu)

st.divider()
# ==================== Charts ====================
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📊 Sentiment Distribution")
    sentiment_counts = df["sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["sentiment", "count"]
    
    colors = {"positive": "#2ecc71", "negative": "#e74c3c", "neutral": "#95a5a6"}
    fig_pie = px.pie(
        sentiment_counts,
        names="sentiment",
        values="count",
        color="sentiment",
        color_discrete_map=colors,
        hole=0.4
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    st.subheader("🏆 Top 10 บุคคลที่ถูกพูดถึงมากที่สุด")
    
    from collections import Counter
    all_persons = []
    for persons in df["persons"]:
        all_persons.extend(persons)
    
    top_persons = Counter(all_persons).most_common(10)
    persons_df = pd.DataFrame(top_persons, columns=["name", "count"])
    
    fig_bar = px.bar(
        persons_df,
        x="count",
        y="name",
        orientation="h",
        color="count",
        color_continuous_scale="blues"
    )
    fig_bar.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()



# ==================== Sentiment per Person ====================

st.subheader("Sentiment ของแต่ละบุคคลที่ถูกกล่าวถึง")

# หาบุคคลที่ปรากฏในแต่ละบทความพร้อม sentiment ของบทความนั้น
person_sentiments = []
for _, row in df.iterrows():
    for person in row["persons"]:
        person_sentiments.append({
            "person": person,
            "sentiment": row["sentiment"],
            "score": row["sentiment_score"]
        })

ps_df = pd.DataFrame(person_sentiments)

if not ps_df.empty:
    # เลือกเฉพาะคนที่ปรากฏมากกว่า 1 ครั้ง
    top_p = ps_df["person"].value_counts()
    top_p = top_p[top_p > 1].index.tolist()
    ps_df = ps_df[ps_df["person"].isin(top_p)]

    fig_sentiment = px.histogram(
        ps_df,
        x="person",
        color="sentiment",
        color_discrete_map=colors,
        barmode="group"
    )

    fig_sentiment.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_sentiment, use_container_width=True)

st.divider()

# ==================== Data Table ====================
st.subheader("📋 ตารางข้อมูลบทความทั้งหมด")

# Filter
sentiment_filter = st.selectbox(
    "กรองตาม Sentiment:",
    ["ทั้งหมด", "positive", "negative", "neutral"]
)

filtered_df = df if sentiment_filter == "ทั้งหมด" else df[df["sentiment"] == sentiment_filter]

st.dataframe(
    filtered_df[["title", "sentiment", "sentiment_score", "Persons_count"]],
    use_container_width=True,
    hide_index=True
)