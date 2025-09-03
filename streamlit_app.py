import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader  # Use PdfReader instead of PdfFileReader

# Show title and description.
st.title("📄 My Document question answering_Shraddha- HW 1")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Ask user for their OpenAI API key
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Allow .txt, .md, and .pdf files
    uploaded_file = st.file_uploader(
        "Upload a document (.txt, .md, or .pdf)", type=("txt", "md", "pdf")
    )

    # Ask the user for a question
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:
        file_extension = uploaded_file.name.split(".")[-1].lower()

        # Handle text or PDF
        if file_extension in ["txt", "md"]:
            document = uploaded_file.read().decode()
        elif file_extension == "pdf":
            pdf_reader = PdfReader(uploaded_file)  # Updated here
            document = ""
            for page in pdf_reader.pages:       # Use `pages` instead of `getPage`
                document += page.extract_text()

        # Prepare messages
        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {question}",
            }
        ]

        # Generate answer
        stream = client.chat.completions.create(
            model="gpt-5-nano",
            messages=messages,
            stream=True,
        )

        st.write_stream(stream)
