import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import pypdf
import os

load_dotenv()

st.title("📄 PDF Chatbot")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# PDF upload
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

# Extract text from PDF
@st.cache_data
def extract_text(file):
    reader = pypdf.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if uploaded_file:
    pdf_text = extract_text(uploaded_file)
    st.success(f"PDF loaded! ({len(pdf_text)} characters)")
    
    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Question input
    if question := st.chat_input("Ask a question about the PDF"):
        # Show user message
        with st.chat_message("user"):
            st.write(question)
        st.session_state.messages.append({"role": "user", "content": question})
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": f"Answer questions based on this PDF content:\n\n{pdf_text[:15000]}"},
                        {"role": "user", "content": question}
                    ]
                )
                answer = response.choices[0].message.content
                st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
else:
    st.info("Please upload a PDF to start chatting.")