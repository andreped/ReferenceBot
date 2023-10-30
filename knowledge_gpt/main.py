import os
os.environ["OPENAI_API_TYPE"] = "azure"  # configure API to Azure OpenAI

import streamlit as st
st.set_page_config(page_title="ReferenceBot", page_icon="📖", layout="wide")

# add all secrets into environmental variables
try:
    for key, value in st.secrets.items():
        os.environ[key] = value
except FileNotFoundError as e:
    print(e)
    print("./streamlit/secrets.toml not found. Assuming secrets are"
          " already available as environmental variables...")


from knowledge_gpt.components.sidebar import sidebar

from knowledge_gpt.ui import (
    wrap_doc_in_html,
    is_query_valid,
    is_file_valid,
    display_file_read_error,
)

from knowledge_gpt.core.caching import bootstrap_caching

from knowledge_gpt.core.parsing import read_file
from knowledge_gpt.core.chunking import chunk_file
from knowledge_gpt.core.embedding import embed_files
from knowledge_gpt.core.qa import query_folder

from langchain.chat_models import AzureChatOpenAI


def main():
    EMBEDDING = "openai"
    VECTOR_STORE = "faiss"
    MODEL_LIST = ["gpt-3.5-turbo", "gpt-4"]

    # Uncomment to enable debug mode
    # MODEL_LIST.insert(0, "debug")

    st.header("📖ReferenceBot")

    # Enable caching for expensive functions
    bootstrap_caching()

    sidebar()

    uploaded_file = st.file_uploader(
        "Upload a pdf, docx, or txt file",
        type=["pdf", "docx", "txt"],
        help="Scanned documents are not supported yet!",
    )

    model: str = st.selectbox("Model", options=MODEL_LIST)  # type: ignore

    with st.expander("Advanced Options"):
        return_all_chunks = st.checkbox("Show all chunks retrieved from vector search")
        show_full_doc = st.checkbox("Show parsed contents of the document")

    if not uploaded_file:
        st.stop()

    try:
        file = read_file(uploaded_file)
    except Exception as e:
        display_file_read_error(e, file_name=uploaded_file.name)

    chunked_file = chunk_file(file, chunk_size=300, chunk_overlap=0)

    if not is_file_valid(file):
        st.stop()

    with st.spinner("Indexing document... This may take a while⏳"):
        folder_index = embed_files(
            files=[chunked_file],
            embedding=EMBEDDING if model != "debug" else "debug",
            vector_store=VECTOR_STORE if model != "debug" else "debug",
            deployment=os.environ["ENGINE_EMBEDDING"],
            model=os.environ["ENGINE"],
            openai_api_key=os.environ["OPENAI_API_KEY"],
            openai_api_base=os.environ["OPENAI_API_BASE"],
            openai_api_type="azure",
            chunk_size = 1,
        )

    with st.form(key="qa_form"):
        query = st.text_area("Ask a question about the document")
        submit = st.form_submit_button("Submit")

    if show_full_doc:
        with st.expander("Document"):
            # Hack to get around st.markdown rendering LaTeX
            st.markdown(f"<p>{wrap_doc_in_html(file.docs)}</p>", unsafe_allow_html=True)

    if submit:
        if not is_query_valid(query):
            st.stop()

        # Output Columns
        answer_col, sources_col = st.columns(2)

        with st.spinner("Setting up AzureChatOpenAI bot..."):
            llm = AzureChatOpenAI(
                openai_api_base=os.environ["OPENAI_API_BASE"],
                openai_api_version=os.environ["OPENAI_API_VERSION"],
                deployment_name=os.environ["ENGINE"],
                openai_api_key=os.environ["OPENAI_API_KEY"],
                openai_api_type="azure",
                temperature=0,
            )
        
        with st.spinner("Querying folder to get result..."):
            result = query_folder(
                folder_index=folder_index,
                query=query,
                return_all=return_all_chunks,
                llm=llm,
            )

        with answer_col:
            st.markdown("#### Answer")
            st.markdown(result.answer)

        with sources_col:
            st.markdown("#### Sources")
            for source in result.sources:
                st.markdown(source.page_content)
                st.markdown(source.metadata["source"])
                st.markdown("---")


if __name__ == "__main__":
    main()
