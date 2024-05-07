import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
import replicate
import requests


load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

prompt_template = """
You are an expert at music generation for running.
Please take the user's request and give a music description for latter music generation.

The user's request is:
I am running {p1} in {p2}, my current running cadence is {p3}, my current heartrate is {p4}, my favorite music genre is {p5}, and now I want a {p6} music.
My running goal is {p7}. Please give me a professional music description so that I can generate a piece of music to assist my current running.

"""

def generate_content(prompt):
    response = model.generate_content(prompt)
    return response.text

st.title("🎵 MusicGen for Running")

col1, col2 = st.columns(2)
with col1:
    location = st.selectbox("Choose your running location:", ["Indoor", "Outdoor"])
    weather = st.selectbox("Choose the weather:", ["Sunny", "Cloudy", "Rainy", "Windy"])
with col2:
    cadence = st.selectbox("Choose your current running cadence:", ["140", "150", "160", "170", "180"])
    heartrate = st.selectbox("Choose your current heartrate:", ["100", "120", "140", "160", "180"])

col3, col4 = st.columns(2)
with col3:
    genre = st.selectbox("Choose your favorite music genre:", ["Rock", "R&B", "Hip-hop", "Jazz", "Classical"])
with col4:
    style = st.selectbox("Choose the music style you want:", ["Cheerful", "Energetic", "Relaxing"])

# Text area for running goals
goals = st.text_area("Enter your running goals:")

audio_file = None

# Button to generate music description
if st.button("Give me a Tempo!"):
    # Formatting the prompt with the selected options and the running goals
    filled_prompt = prompt_template.format(p1=location, p2=weather, p3=cadence, p4=heartrate, p5=genre, p6=style, p7=goals)
    reply = generate_content(filled_prompt)
    st.write(reply)

    st.download_button(label="Download Music Prompt", data=reply, file_name="Music_Prompt.txt", mime="text/plain")

    with st.spinner("Generating music might take up to 2 minutes. Please wait..."):
            output_url = replicate.run(
                "meta/musicgen:671ac645ce5e552cc63a54a2bbff63fcf798043055d2dac5fc9e36a837eedcfb",
                input={
                    "top_k": 250,
                    "top_p": 0,
                    "prompt": reply,
                    "duration": 30,
                    "temperature": 1,
                    "continuation": False,
                    "model_version": "stereo-large",
                    "output_format": "mp3",
                    "continuation_start": 0,
                    "multi_band_diffusion": False,
                    "normalization_strategy": "peak",
                    "classifier_free_guidance": 3
                }
            )

    audio_file_path = "generated_music.mp3"
    response = requests.get(output_url, stream=True)
    if response.status_code == 200:
        with open(audio_file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)

        audio_file = audio_file_path

if audio_file:
    st.audio(audio_file, format="audio/mp3")