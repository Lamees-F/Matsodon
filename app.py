# streamlit_mastodon_dashboard.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(
    page_title="Mastodon Trending Hashtags Dashboard",
    layout="wide",
    page_icon="📊"
)

# ------------------------------
# Title & Description
# ------------------------------
st.title("Mastodon Trending Hashtags Analysis")
st.markdown("""
This interactive dashboard allows you to explore trending hashtags on Mastodon.
You can visualize their usage over time, inspect the data, and see a word cloud representing today's trends.
The data is loaded from a pre-saved CSV file in the `data/` directory.
""")

# ------------------------------
# Load Data

# Read CSV
df = pd.read_csv("data/mastodon_hashtags_raw.csv")

# Ensure 'date' column is datetime
df['date'] = pd.to_datetime(df['date'])

# ------------------------------
# Sidebar Controls
# ------------------------------
st.sidebar.header("Controls")
top_n = st.sidebar.slider("Number of top hashtags to display in word cloud", min_value=5, max_value=50, value=20)
selected_hashtag = st.sidebar.selectbox("Select a hashtag to track over time", sorted(df['hashtag'].unique()))

# ------------------------------
# Word Cloud
# ------------------------------
st.subheader("Trending Hashtags Word Cloud (Today)")

# Filter for today's data
today = df['date'].max()
df_today = df[df['date'] == today]
hashtag_freq = {row['hashtag']: int(row['uses']) for _, row in df_today.nlargest(top_n, 'uses').iterrows() if int(row['uses']) > 0}

# Japanese-capable font (adjust path if needed)
font_path = "C:/Windows/Fonts/msgothic.ttc"

wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='white',
).generate_from_frequencies(hashtag_freq)

plt.figure(figsize=(12,6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
st.pyplot(plt)

# ------------------------------
# Hashtag Usage Over Time
# ------------------------------
st.subheader(f"Daily Usage Trend for #{selected_hashtag}")
df_topic = df[df['hashtag'] == selected_hashtag].sort_values('date')
plt.figure(figsize=(10,5))
plt.plot(df_topic['date'], df_topic['uses'], marker='o', linestyle='-')
plt.title(f"Daily Usage Trend: #{selected_hashtag}")
plt.xlabel("Date")
plt.ylabel("Uses")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)

# ------------------------------
# Display Raw Data
# ------------------------------
st.subheader("Trending Hashtags Data")
st.dataframe(df.sort_values(['date','uses'], ascending=[False, False]))
