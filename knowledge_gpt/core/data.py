import streamlit as st
from gdown import download_folder


@st.cache_resource(show_spinner=False)
def download_test_data():
    # url = f"https://drive.google.com/drive/folders/uc?export=download&confirm=pbef&id={file_id}"
    url = "https://drive.google.com/drive/folders/1uDSAWtLvp1YPzfXUsK_v6DeWta16pq6y"
    with st.spinner(text="Downloading test data. This might take a minute."):
        # @TODO: replace gown solution with a custom solution compatible with GitHub and
        # use st.progress to get more verbose during download
        download_folder(url=url, quiet=False, use_cookies=False, output="./data/")
