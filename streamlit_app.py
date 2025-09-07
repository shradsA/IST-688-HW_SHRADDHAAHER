import streamlit as st
<<<<<<< HEAD
from hws.hw1 import run_hw1
from hws.hw2 import run_hw2

st.set_page_config(page_title="HW Manager")
st.title("📚 HW Manager")
st.write("Select a page from the sidebar to continue.")

pages = {
    "HW1 - Document Q&A": run_hw1,
    "HW2 - URL Summarizer": run_hw2,
}

choice = st.sidebar.selectbox("Choose a page", list(pages.keys()))

pages[choice]()
=======
from openai import OpenAI
import PyPDF2
import time

st.title("My Document_Shraddha - HW 1")
st.write(
    "Upload a `.txt` or `.pdf` file and ask a question about it – "
    "answers will be shown from 4 different models for comparison."
)

# -------------------------------
# API Key
# -------------------------------
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")
    st.stop()

client = OpenAI(api_key=openai_api_key)

# -------------------------------
# File Uploader
# -------------------------------
uploaded_file = st.file_uploader("Upload a document (.txt or .pdf)", type=("txt", "pdf"))

# clear document if file is removed
if "document_text" not in st.session_state:
    st.session_state.document_text = ""

if uploaded_file is None:
    st.session_state.document_text = ""
else:
    file_extension = uploaded_file.name.split('.')[-1].lower()
    document_text = ""
    if file_extension == "txt":
        try:
            document_text = uploaded_file.read().decode("utf-8")
        except Exception:
            document_text = str(uploaded_file.read())
    elif file_extension == "pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            document_text += page.extract_text() or ""
    else:
        st.error("Unsupported file type!")
        st.stop()

    # truncate to avoid long context
    MAX_CHARS = 3000
    if len(document_text) > MAX_CHARS:
        document_text = document_text[:MAX_CHARS]
        st.warning("Document is large; only the first part is used.")
    st.session_state.document_text = document_text

# -------------------------------
# Question Input
# -------------------------------
question = st.text_area(
    "Ask a question about the document!",
    placeholder="Example: Is this course hard?",
    disabled=(uploaded_file is None),
)

# -------------------------------
# Run Button
# -------------------------------
if st.button("Get Answers from All Models"):
    if not st.session_state.document_text:
        st.error("No document available. Please upload a file.")
    elif not question.strip():
        st.error("Please type a question.")
    else:
        doc = st.session_state.document_text
        prompt = f"Here is a document:\n\n{doc}\n\nQuestion: {question}\n\nAnswer clearly and concisely."

        models = [
            "gpt-3.5-turbo",
            "gpt-4.1",
            "gpt-5-chat-latest",
            "gpt-5-nano"
        ]
        results = {}

        for m in models:
            with st.spinner(f"Calling {m}..."):
                start = time.time()
                try:
                    response = client.chat.completions.create(
                        model=m,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    elapsed = time.time() - start
                    text = response.choices[0].message.content
                    results[m] = {"answer": text, "time": elapsed}
                except Exception as e:
                    results[m] = {"answer": f"Error: {e}", "time": None}

        # -------------------------------
        # Display Results
        # -------------------------------
        tabs = st.tabs(models)
        for tab, m in zip(tabs, models):
            with tab:
                st.subheader(f"Model: {m}")
                if results[m]["time"]:
                    st.write(f"**Elapsed time:** {results[m]['time']:.2f} seconds")
                st.markdown("**Answer:**")
                st.write(results[m]["answer"])
>>>>>>> 03dccc8 (HW2.0)
