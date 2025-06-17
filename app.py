import streamlit as st
import os
from dotenv import load_dotenv

from utils.file_loader import extract_text
from utils.chunker import chunk_text
from utils.embedder import get_embeddings
from utils.retriever import VectorStore
from utils.responder import generate_answer
from utils.feedback import create_feedback_entry, save_feedback

# Init
load_dotenv()
st.set_page_config(page_title="GenAI Document Query", layout="wide")
st.title("📄 GenAI Document Query Assistant")

# Upload files
uploaded_files = st.file_uploader("Upload documents (PDF, DOCX, TXT, CSV)", type=["pdf", "docx", "txt", "csv"], accept_multiple_files=True)

if uploaded_files:
    all_text = ""
    for file in uploaded_files:
        with st.spinner(f"Processing {file.name}..."):
            raw_text = extract_text(file)
            all_text += raw_text + "\n"

    # Chunking
    chunks = chunk_text(all_text, chunk_size=500, overlap=100)
    st.success(f"Extracted and chunked {len(chunks)} text blocks.")

    # Embeddings
    with st.spinner("Generating embeddings..."):
        embeddings = get_embeddings(chunks)

    if not embeddings or not isinstance(embeddings[0], list):
        st.error("❌ Failed to generate embeddings. Check your model setup or input.")
        st.stop()

    store = VectorStore(dimension=len(embeddings[0]))
    store.add_embeddings(embeddings, chunks)

    # User Query
    user_query = st.text_input("Ask a question about your documents:")
    if user_query:
        query_embedding = get_embeddings([user_query])[0]
        retrieved_chunks = store.query(query_embedding, top_k=5)
        context = "\n".join(retrieved_chunks)

        # Generate answer with Groq LLM
        with st.spinner("Generating response..."):
            answer = generate_answer(context, user_query)
        st.markdown("### 🤖 Suggested Response")
        st.write(answer)

        # Feedback
        st.markdown("---")
        st.markdown("### 🔁 Was this helpful?")
        feedback = st.radio("Your feedback:", ["👍", "👎"], horizontal=True)

        clarification = None
        if feedback == "👎":
            clarification = st.text_area("What could be improved?")

        if st.button("Submit Feedback"):
            entry = create_feedback_entry(user_query, answer, feedback, clarification)
            save_feedback(entry)
            st.success("✅ Feedback saved. Thank you!")

            if clarification:
                # Retry with user input
                updated_context = context + f"\n\nUser clarification: {clarification}"
                with st.spinner("Refining answer..."):
                    updated_answer = generate_answer(updated_context, user_query)
                st.markdown("### 🔁 Updated Response")
                st.write(updated_answer)
