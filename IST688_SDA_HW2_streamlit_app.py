# streamlit_app.py
import streamlit as st
import importlib.util
import runpy
from pathlib import Path

st.set_page_config(page_title="HW Manager")
st.title("📚 HW Manager")
st.write("Select a page from the sidebar to continue.")

PAGES_DIR = Path("HWs")
pages = {
    "HW1 - Document Q&A": PAGES_DIR / "HW1.py",
    "HW2 - URL Summarizer": PAGES_DIR / "HW2.py",
}

choice = st.sidebar.selectbox("Choose a page", list(pages.keys()))

page_path = pages[choice]

# Execute the selected page file in its own namespace.
# Using runpy.run_path isolates the page's variables from streamlit_app.py.
runpy.run_path(str(page_path), run_name="__main__")

