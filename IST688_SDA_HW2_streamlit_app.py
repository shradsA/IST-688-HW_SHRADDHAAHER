import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.resolve()))

import streamlit as st
from hw1 import run_hw1
from hw2 import run_hw2

st.set_page_config(page_title="HW Manager")
st.title("📚 HW Manager")
st.write("Select a page from the sidebar to continue.")

pages = {
    "HW1 - Document Q&A": run_hw1,
    "HW2 - URL Summarizer": run_hw2,
}

choice = st.sidebar.selectbox("Choose a page", list(pages.keys()))

# Run selected page
pages[choice]()
