# Import from standard library
import os
import logging

# Import from 3rd party libraries
import streamlit as st

# Import modules from the local package
from eleven_labs import with_custom_voice, with_premade_voice, get_voices
from _langchain import get_response


def generate_podcast_text(prompt, podcaster, guest,):
    return get_response(prompt, podcaster, guest)


def generate_podcast(voice, prompt, podcaster, guest,):
    with text_spinner_placeholder:
        with st.spinner("Please wait while we process your query..."):
            g_podcast = generate_podcast_text(prompt, podcaster, guest,)

            st.session_state.prompt_generate = (g_podcast)

            audio_path = with_premade_voice(prompt=g_podcast, voice=voice)

            if audio_path != "":
                st.session_state.file_path = audio_path


def generate_podcast_demo(p, v):
    st.session_state.podcast_generate = p

    p = with_premade_voice(prompt=p, voice=v)
    
    
    if p != "":
        st.session_state.file_path = p



# Configure logger
logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)


# Configure Streamlit page and state
st.set_page_config(page_title="iPodcast", page_icon="🎧")


# Store the initial value of widgets in session state
if "podcast_generate" not in st.session_state:
    st.session_state.podcast_generate = ""

if "file_path" not in st.session_state:
    st.session_state.file_path = ""

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"



# Force responsive layout for columns also on mobile
st.write(
    """
    <style>
    [data-testid="column"] {
        width: calc(50% - 1rem);
        flex: 1 1 calc(50% - 1rem);
        min-width: calc(50% - 1rem);
    }
    </style>
    """,
    unsafe_allow_html=True,
)



# Render Streamlit page


# title of the app
st.title("Eleven Labs + Langchain Tutorial")


# brief description of the app
st.markdown(
    "This is a demo of the Eleven Labs + Langchain Tutorial."
)


# header
# st.header("This is a demo of the Eleven Labs + Langchain Tutorial")


# file upload if you want to use custom voice
# file = st.file_uploader(label="Upload file", type=["mp3",])
# if file is not None:
#     filename = "sample.mp3"
#     with open(filename, "wb") as f:
#         f.write(file.getbuffer())
#     st.session_state.file_path = "sample.mp3"


# selectbox
voice = st.selectbox('Choose your voice', (i for i in get_voices()))


col1, col2 = st.columns(2)

with col1:
    podcaster = st.text_input(label="Podcaster", placeholder="Ex. Lex Fridman")

with col2:
    guest = st.text_input(label="Guest", placeholder="Ex. Elon Musk")



# textarea
prompt = st.text_area(label="Podcast info", placeholder="Ex. Elon Musk joins Lex Fridman in conversation about AI, Autopilot, Neuralink, Tesla, and his personal history.", height=100)


# button
st.button(
    label="Generate Podcast",
    help="Click to generate podcast",
    key="generate_podcast",
    type="primary",
    on_click=generate_podcast,
    args=(voice, prompt, podcaster, guest,),
)

# button
st.button(
    label="demo",
    help="demo",
    key="generate_podcast_demo",
    type="primary",
    on_click=generate_podcast_demo,
    args=("Hi! My name is Bella, nice to meet you!", voice,)
)


text_spinner_placeholder = st.empty()
if st.session_state.text_error:
    st.error(st.session_state.text_error)


if st.session_state.podcast_generate:
    st.markdown("""---""")
    st.subheader("Read Podcast")
    st.text_area(label="You may read podcast while audio being generated.", value=st.session_state.podcast_generate,)


if st.session_state.file_path:
    st.markdown("""---""")
    st.subheader("Listen to Podcast")

    with open(st.session_state.file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()

    st.audio(audio_bytes, format='audio/mp3', start_time=0)