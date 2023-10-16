import os
import sys

import django
import streamlit as st
from PIL import Image


def init_django():
    sys.path.append(".")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    django.setup()


init_django()

import utils  # noqa

st.set_page_config(layout="wide", page_title="Llama Explorer", page_icon="🦙")

st.markdown(
    """
    <meta name="description" content="🚀 Get instant insights in the open-source AI landscape. Most starred repositories, top contirbutors and most used programming languages in a single simple UI.">
    """,  # noqa E501
    unsafe_allow_html=True,
)

st.markdown(
    """
# 🦙 Llama Explorer
#### 🤙 Instant insights into open source AI projects and contributors
"""
)

image = Image.open("./assets/cover.jpeg")
st.image(image, caption="Llama Explorer on Mars")

st.divider()

metric1, metric2, metric3 = utils.fetch_basic_metrics()

col1, col2, col3 = st.columns(3)
col1.metric("Repositories Tracked", metric1)
col2.metric("Most used Programming Language", metric2)
col3.metric("Location with the most Contributors", metric3)

st.divider()

st.markdown(
    """
### Most active Contributor today
"""
)

metric1, metric2, metric3 = utils.fetch_best_contributor_of_the_day()

col1, col2, col3 = st.columns(3)

col1.metric("🤖 Username", metric1)
col2.metric("💻 Commits", metric2)
col3.image(
    metric3,
    caption=metric1,
    use_column_width=True,
)

st.divider()

df_repos = utils.fetch_most_starred_repositories()

st.markdown("### ⭐️ Most Starred Repositories")
st.dataframe(df_repos, use_container_width=True, hide_index=False)

st.divider()

df_contributors = utils.fetch_most_active_contributors()

st.markdown("### 🤖 Most Active Contributors")
st.dataframe(df_contributors, use_container_width=True, hide_index=True)


df = utils.fetch_contributors_locations()

st.map(df, size=30, zoom=1, use_container_width=True)

st.divider()

chart_data = utils.fetch_most_used_programming_languages()

st.markdown("### 🦀 Most Used Programming Languages")
chart = st.bar_chart(
    chart_data.set_index("Programming Language"), use_container_width=True
)

st.markdown(
    """
> Data is fetched everyday at 00:00 UTC. If you don't see a repository, you can create a PR to add it to the list. Check how to do that in the settings page.
"""  # noqa E501
)
