import streamlit as st
from hws.hw1 import run_hw1
from hws.hw2 import run_hw2

st.set_page_config(page_title="HW Manager")

pages = {
    "HW1 - Document Q&A": run_hw1,
    "HW2 - URL Summarizer": run_hw2,
}

choice = st.sidebar.selectbox("Choose a page", list(pages.keys()))

pages[choice]()
