import os
import tempfile

import streamlit as st
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

st.title("Simple RAG App")

if not api_key:
    st.error("OPENAI_API_KEY not found. Add it to your ..env file.")
    st.stop()

# 1. Session state
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "file_name" not in st.session_state:
    st.session_state.file_name = None

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

# 2. (Re)build the vector store when a new file is uploaded
if uploaded_file and uploaded_file.name != st.session_state.file_name:
    with st.spinner("Processing PDF..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.getbuffer())
            tmp_path = tmp.name
        try:
            documents = PyPDFLoader(tmp_path).load()
        finally:
            os.remove(tmp_path)

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key)
        st.session_state.vectorstore = FAISS.from_documents(docs, embeddings)
        st.session_state.file_name = uploaded_file.name
        st.success("Vector DB Created!")

# 3. Query
query = st.text_input("Ask something about your PDF")

if query:
    if st.session_state.vectorstore is None:
        st.info("Please upload a PDF first.")
    else:
        llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)
        retriever = st.session_state.vectorstore.as_retriever()

        prompt = ChatPromptTemplate.from_template(
            "Answer the question using only the context below. "
            "If the answer is not in the context, say you don't know.\n\n"
            "Context:\n{context}\n\nQuestion: {question}"
        )
        chain = prompt | llm | StrOutputParser()

        with st.spinner("Thinking..."):
            context_docs = retriever.invoke(query)
            context = "\n\n".join(d.page_content for d in context_docs)
            answer = chain.invoke({"context": context, "question": query})

        st.write("**Answer:**")
        st.write(answer)
