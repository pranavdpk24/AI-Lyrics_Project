import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000/generate"

st.set_page_config(
    page_title="AI Song Lyrics Generator",
    page_icon="🎵",
    layout="centered"
)

st.title("🎵 AI Song Lyrics Generator")

st.write("Generate unique AI-powered song lyrics using Google Gemini.")

theme = st.text_input("Theme")

story = st.text_area("Story / Background")

genre = st.selectbox(
    "Genre",
    [
        "Pop",
        "Rock",
        "Rap",
        "Country",
        "R&B"
    ]
)

if st.button("Generate Lyrics"):

    if theme == "" or story == "":
        st.warning("Please fill out Theme and Story.")

    else:

        payload = {
            "theme": theme,
            "story": story,
            "genre": genre
        }

        try:

            with st.spinner("Generating lyrics..."):

                response = requests.post(
                    BACKEND_URL,
                    json=payload
                )

            if response.status_code == 200:

                lyrics = response.json()["lyrics"]

                st.success("Lyrics Generated!")

                st.text_area(
                    "Generated Lyrics",
                    lyrics,
                    height=500
                )

            else:
                st.error("Backend returned an error.")

        except Exception as e:

            st.error(f"Unable to connect to backend.\n\n{e}")