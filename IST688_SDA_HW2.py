import streamlit as st
from openai import OpenAI
import cohere
import requests
from bs4 import BeautifulSoup
import time

# -------------------------------
# Optional Groq import
# -------------------------------
try:
    from groq import Groq
    groq_available = True
except ModuleNotFoundError:
    groq_available = False
    st.warning("Groq SDK not installed. Groq option will not be available.")

# -------------------------------
# Helper function: read URL
# -------------------------------
def read_url_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text(separator="\n")
    except requests.RequestException as e:
        st.error(f"Error reading {url}: {e}")
        return None

# -------------------------------
# Page Title
# -------------------------------
st.title("HW2 - URL Summarizer")
st.write("Enter a web page URL, choose summary type, language, and LLM to use.")

# -------------------------------
# Load API Keys from secrets.toml
# -------------------------------
openai_api_key = st.secrets.get("OPENAI_API_KEY")
cohere_api_key = st.secrets.get("COHERE_API_KEY")
groq_api_key = st.secrets.get("GROQ_API_KEY") if groq_available else None

# -------------------------------
# Sidebar Controls
# -------------------------------
st.sidebar.header("⚙️ Settings")
summary_type = st.sidebar.selectbox(
    "📑 Type of Summary",
    ["Short Summary", "Detailed Summary", "Bullet Points"]
)
output_language = st.sidebar.selectbox(
    "🌍 Output Language",
    ["English", "French", "Spanish"]
)

# LLM options
llm_options = ["OpenAI (gpt-4.1)", "Cohere (command-r-plus)"]
if groq_available:
    llm_options.append("Groq (llama-3.3-70b-versatile)")
llm_choice = st.sidebar.selectbox("🤖 Choose LLM", llm_options)

# -------------------------------
# URL Input
# -------------------------------
url = st.text_input("🌐 Enter a webpage URL", placeholder="https://example.com")

# -------------------------------
# Run Button
# -------------------------------
if st.button("Summarize URL"):
    if not url.strip():
        st.error("Please enter a valid URL.")
    else:
        with st.spinner("Reading webpage..."):
            content = read_url_content(url)

        if not content:
            st.error("Failed to retrieve content.")
        else:
            MAX_CHARS = 4000
            if len(content) > MAX_CHARS:
                content = content[:MAX_CHARS]
                st.warning("Webpage is large; only the first part is summarized.")

            prompt = f"""
You are a helpful assistant. Read the following webpage content and provide a {summary_type}.
Make sure your response is in {output_language}.

Webpage Content:
{content}
"""

            start_time = time.time()
            answer = "Not implemented."

            try:
                if llm_choice.startswith("OpenAI"):
                    client = OpenAI(api_key=openai_api_key)
                    response = client.chat.completions.create(
                        model="gpt-4.1",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    answer = response.choices[0].message.content

                elif llm_choice.startswith("Cohere"):
                    client = cohere.Client(api_key=cohere_api_key)
                    response = client.chat(model="command-r-plus", message=prompt)
                    answer = response.text

                elif llm_choice.startswith("Groq"):
                    if not groq_api_key:
                        answer = "Groq API key not found."
                    else:
                        client = Groq(api_key=groq_api_key)
                        response = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",  # <- updated model
                            messages=[{"role": "user", "content": prompt}]
                        )
                        answer = response.choices[0].message.content

            except Exception as e:
                answer = f"Error: {e}"

            elapsed = time.time() - start_time

            # -------------------------------
            # Display Results
            # -------------------------------
            st.subheader(f"Summary ({llm_choice})")
            st.write(f"**Elapsed time:** {elapsed:.2f} seconds")
            st.markdown("**Result:**")
            st.write(answer)
