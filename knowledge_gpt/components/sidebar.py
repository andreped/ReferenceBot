import streamlit as st

from dotenv import load_dotenv

load_dotenv()


def sidebar():
    with st.sidebar:
        st.markdown("# About")
        st.markdown(
            "📖ReferenceBot allows you to ask questions about your "
            "documents and get accurate answers with instant citations. "
        )
        st.markdown(
            "This tool is a work in progress. "
            "You can contribute to the project on [GitHub](https://github.com/andreped/ReferenceBot) "  # noqa: E501
            "with your feedback and suggestions💡"
        )
        st.markdown("The tool was based on KnowledgeGPT made by [mmz_001](https://twitter.com/mm_sasmitha).")
        st.markdown("---")

        # faq()
