# streamlit_mastodon_dashboard.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(
    page_title="Mastodon Insights Dashboard",
    layout="wide",
    page_icon="🦣"
)

# ------------------------------
# Mastodon-style Header
# ------------------------------
st.markdown(
    """
    <div style="background-color:#6366F1; padding:20px; border-radius:10px; text-align:center">
        <h1 style="color:white; font-family:'MS Gothic', sans-serif;">🦣 Mastodon Insights Dashboard</h1>
        <p style="color:white; font-size:18px; font-family:'MS Gothic', sans-serif;">
        Explore trending hashtags and posting patterns on Mastodon in real-time.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ------------------------------
# Load Data
# ------------------------------
df = pd.read_csv("data/mastodon_hashtags_raw.csv")
df['date'] = pd.to_datetime(df['date'])

df_post = pd.read_csv("data/mastodon_posts.csv")
df_post['created_at'] = pd.to_datetime(df_post['created_at'], utc=True)
df_post['hour'] = df_post['created_at'].dt.hour
df_post['day_of_week'] = df_post['created_at'].dt.day_name()

# ------------------------------
# Sidebar Controls
# ------------------------------
st.sidebar.header("Dashboard Controls")
top_n = st.sidebar.slider("Number of top hashtags for word cloud", min_value=5, max_value=50, value=20)
selected_hashtag = st.sidebar.selectbox("Select a hashtag to track over time", sorted(df['hashtag'].unique()))

st.sidebar.markdown("---")
st.sidebar.header("Team Members")
st.sidebar.markdown("Deena, Lamees, Laura")
st.sidebar.markdown("[GitHub Repository](https://github.com/Lamees-F/Matsodon)")

# ------------------------------
# Word Cloud Section
# ------------------------------
st.subheader("Trending Hashtags Word Cloud 🌐")

today = df['date'].max()
df_today = df[df['date'] == today]
hashtag_freq = {row['hashtag']: int(row['uses']) for _, row in df_today.nlargest(top_n, 'uses').iterrows() if int(row['uses']) > 0}

wordcloud = WordCloud(
    width=900,
    height=450,
    background_color='white',
    colormap='Blues',
    font_path="C:/Windows/Fonts/msgothic.ttc"  # Japanese-capable font
).generate_from_frequencies(hashtag_freq)

plt.figure(figsize=(12,6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
st.pyplot(plt)
plt.clf()

# ------------------------------
# Hashtag Usage Over Time
# ------------------------------
st.subheader(f"Daily Usage Trend for #{selected_hashtag} 📈")
df_topic = df[df['hashtag'] == selected_hashtag].sort_values('date')

plt.figure(figsize=(10,5))
plt.plot(df_topic['date'], df_topic['uses'], marker='o', linestyle='-', color='#6366F1')
plt.fill_between(df_topic['date'], df_topic['uses'], color='#6366F1', alpha=0.1)
plt.title(f"Daily Usage Trend: #{selected_hashtag}", fontname="MS Gothic")
plt.xlabel("Date", fontname="MS Gothic")
plt.ylabel("Uses", fontname="MS Gothic")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)
plt.clf()

# ------------------------------
# Posts by Hour of Day (Plotly)
# ------------------------------
st.subheader("🕒 Posts by Hour of the Day")

posts_per_hour = df_post.groupby('hour').size().sort_index().reset_index(name='count')
peak_hour = posts_per_hour.loc[posts_per_hour['count'].idxmax(), 'hour']

fig_hour = px.bar(
    posts_per_hour,
    x='hour',
    y='count',
    text='count',
    color='count',
    color_continuous_scale=['#6366F1', '#7C3AED'],
    labels={'hour':'Hour of Day', 'count':'Number of Posts'}
)
st.plotly_chart(fig_hour, use_container_width=True)

# ------------------------------
# Posts by Day of Week (Plotly)
# ------------------------------
st.subheader("📅 Posts by Day of the Week ")

weekday_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
posts_per_day = df_post['day_of_week'].value_counts().reindex(weekday_order).fillna(0).reset_index()
posts_per_day.columns = ['day', 'count']
peak_day = posts_per_day.loc[posts_per_day['count'].idxmax(), 'day']

fig_day = px.bar(
    posts_per_day,
    x='day',
    y='count',
    text='count',
    color='count',
    color_continuous_scale=['#6366F1', '#7C3AED'],
    labels={'day':'Day of Week', 'count':'Number of Posts'}
)
st.plotly_chart(fig_day, use_container_width=True)

