import os
import sys

import django
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

sys.path.append(".")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

st.set_page_config(layout="wide")

st.markdown(
    """
# 🦙 Llama Explorer
#### 🤙 Instant insights into open source AI projects and contributors
"""
)

image = Image.open("./assets/cover.jpeg")
st.image(image, caption="Llama Explorer on Mars")

st.divider()

col1, col2, col3 = st.columns(3)
col1.metric("Number of Repositories Tracked", "120", "3")
col2.metric("Most used Programming Language", "Python")
col3.metric("Country with the Most contributors", "Italy")

st.divider()

st.markdown(
    """
### Best Contributor of the Day
"""
)

col1, col2, col3 = st.columns(3)

col1.metric("🤖 Username", "filopedraz")
col2.metric("💻 Commits", "120", "3")
col3.image(
    "https://avatars.githubusercontent.com/u/29598954",
    caption="filopedraz",
    use_column_width=True,
)

st.divider()

df_repos = pd.DataFrame(
    np.random.randn(50, 4), columns=["Repository", "Stars", "Forks", "Contributors"]
)
st.markdown("### ⭐️ Most Starred Repositories")
st.dataframe(df_repos, use_container_width=True, hide_index=True)

st.divider()

df_contributors = pd.DataFrame(
    np.random.randn(50, 3), columns=["Username", "Commits", "Projects"]
)

st.markdown("### 🤖 Most Active Contributors")
st.dataframe(df_contributors, use_container_width=True, hide_index=True)

st.markdown(
    """
> Data is fetched everyday at 00:00 UTC. If you don't see a repository, you can create PR to add it to the list.
"""
)
