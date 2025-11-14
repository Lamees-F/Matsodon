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
    <div style="background-color:#6366F1; padding:25px; border-radius:10px; text-align:center">
        <h1 style="color:white; font-family:'MS Gothic', sans-serif;">🦣 MastoScope Dashboard</h1>
        <p style="color:white; font-size:20px; font-family:'MS Gothic', sans-serif;">
        Discover the pulse of Mastodon like never before!  
        Monitor trending hashtags, track user engagement, and uncover actionable insights in real-time.  
        Turn raw social media activity into a strategic advantage for your brand.
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

# df_post = pd.read_csv("data/mastodon_posts.csv")
# df_post['created_at'] = pd.to_datetime(df_post['created_at'], utc=True)
# df_post['hour'] = df_post['created_at'].dt.hour
# df_post['day_of_week'] = df_post['created_at'].dt.day_name()

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
# st.subheader("🕒 Posts by Hour of the Day")

# posts_per_hour = df_post.groupby('hour').size().sort_index().reset_index(name='count')
# peak_hour = posts_per_hour.loc[posts_per_hour['count'].idxmax(), 'hour']

# fig_hour = px.bar(
#     posts_per_hour,
#     x='hour',
#     y='count',
#     text='count',
#     color='count',
#     color_continuous_scale=['#6366F1', '#7C3AED'],
#     labels={'hour':'Hour of Day', 'count':'Number of Posts'}
# )
# st.plotly_chart(fig_hour, use_container_width=True)

# # ------------------------------
# # Posts by Day of Week (Plotly)
# # ------------------------------
# st.subheader("📅 Posts by Day of the Week ")

# weekday_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
# posts_per_day = df_post['day_of_week'].value_counts().reindex(weekday_order).fillna(0).reset_index()
# posts_per_day.columns = ['day', 'count']
# peak_day = posts_per_day.loc[posts_per_day['count'].idxmax(), 'day']

# fig_day = px.bar(
#     posts_per_day,
#     x='day',
#     y='count',
#     text='count',
#     color='count',
#     color_continuous_scale=['#6366F1', '#7C3AED'],
#     labels={'day':'Day of Week', 'count':'Number of Posts'}
# )
# st.plotly_chart(fig_day, use_container_width=True)
# ==========================================================
# 🧭 User Insights (Interactive Plotly Visualizations)
# ==========================================================
st.header("User Insights (Interactive Plotly Visualizations)")
st.markdown("""
Explore user-level patterns derived from Mastodon activity data.  
These interactive charts offer deeper insight into user behavior, engagement, and influence.
""")

try:
    # ------------------------------
    # Load user data from Google Drive
    # ------------------------------
    orig_url = 'https://drive.google.com/file/d/1QsnE86MUndd8NpQWu1UVtnJSXcWg-Vqd/view?usp=sharing'
    file_id = orig_url.split('/')[-2]
    dwn_url = 'https://drive.google.com/uc?export=download&id=' + file_id

    user_df = pd.read_csv(
        dwn_url,
        sep=None,
        engine='python',
        on_bad_lines='skip'
    )

    # ------------------------------
    # Scatter: Followers vs Following
    # ------------------------------
    st.subheader("Followers vs Following 🧑‍🤝‍🧑")
    fig = px.scatter(
        user_df,
        x="following_count",
        y="followers_count",
        hover_name="username",
        color="user_type",
        size="statuses_count",
        log_x=True,
        log_y=True,
        range_x=[1, 10_000_000],
        range_y=[1, 10_000_000]
    )
    fig.update_traces(marker=dict(opacity=0.6, size=8))
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    # ------------------------------
    # Scatter: Followers vs Account Age
    # ------------------------------
    st.subheader("Followers vs Account Age ⏳")
    fig = px.scatter(
        user_df,
        x="account_age_days",
        y="followers_count",
        color="user_type",
        hover_name="username",
        log_x=True,
        log_y=True,
        title="Followers vs Account Age (interactive log–log)",
        labels={"account_age_days": "Account Age (days)", "followers_count": "Followers"}
    )
    fig.update_traces(marker=dict(opacity=0.6, size=8))
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

  
        # ------------------------------
        # Boxplot: Follower Count by Top Tags
        # ------------------------------
    tags_df = user_df[['username', 'followers_count', 'featured_tags']].dropna(subset=['featured_tags']).copy()
    tags_df = tags_df.assign(featured_tags=tags_df['featured_tags'].str.split(',')).explode('featured_tags')
    tags_df['featured_tags'] = tags_df['featured_tags'].str.strip().str.lower()

    top_tags = tags_df['featured_tags'].value_counts().head(15).index
    filtered_tags_df = tags_df[tags_df['featured_tags'].isin(top_tags)]

    st.subheader("Follower Count Distribution by Top 15 Featured Tags 📊")
    fig = px.box(
            filtered_tags_df,
            x="featured_tags",
            y="followers_count",
            log_y=True,
            points="all",
            title="Follower Count Distribution by Top 15 Featured Tags",
            labels={"featured_tags": "Featured Tag", "followers_count": "Followers (log scale)"},
        )
    fig.update_traces(marker=dict(opacity=0.5, size=5))
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"❌ Failed to load user dataset or generate visuals: {e}")

# ------------------------------
# Closing Pitch Section
# ------------------------------
st.markdown(
    """
    <div style="background-color:#E0E7FF; padding:20px; border-radius:10px; margin-top:30px;">
        <h2 style="color:#4F46E5; font-family:'MS Gothic', sans-serif;">Why Choose MastoScope?</h2>
        <ul style="color:#1E293B; font-size:16px; font-family:'MS Gothic', sans-serif;">
            <li>📊 Real-time insights into Mastodon trends and user behavior.</li>
            <li>🚀 Interactive, intuitive dashboards for faster decision-making.</li>
            <li>🔍 Identify influential users and top-performing hashtags effortlessly.</li>
            <li>⚡ Turn social media data into actionable strategies for your brand.</li>
        </ul>
        <h3 style="color:#4F46E5; font-family:'MS Gothic', sans-serif;">⚠️Coming Soon:</h3>
        <p style="color:#1E293B; font-size:16px; font-family:'MS Gothic', sans-serif;">
        The <b>Best Time to Post</b> feature! Optimize your content timing based on peak user engagement and trending activity—so your posts reach the right audience at the right time.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


