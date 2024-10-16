import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()  # Load all the environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are a YouTube video summarizer. You will take the transcript text
and summarize the entire video, providing the important points within 250 words.
Please provide the summary of the text given here:  """


# Function to get the transcript data from YouTube videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e


# Function to get the summary based on the prompt from Google Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text


# Inject CSS directly into the app
st.markdown(
    """
    <style>
    body {
        background-color: #f8f9fa;
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
    
    h1 {
        color: #dc3545;
        margin-bottom: 15px;
        font-size: 28px;
    }
    .input-box {
        width: 100%;
        padding: 12px;
        margin-top: 10px;
        border: 1px solid #ced4da;
        border-radius: 5px;
        font-size: 20px;
    }
    .submit-button {
        background-color: #dc3545;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 12px 20px;
        font-size: 20px;
        margin-top: 10px;
        cursor: pointer;
    }
    .submit-button:hover {
        background-color: #c82333;
    }
    .red-summary-box {
        margin-top: 20px;
        padding: 15px;
        border-radius: 10px;
        background-color: #dc3545;
        color: white;
        text-align: left;
        font-size: 15px;
        line-height: 1.6;
    }
    .powered {
        margin-top: 30px;
        font-size: 20px;
        color: #666;
    }
    .no-space-top {
        margin-top: 0px !important; /* Removes unnecessary space on top */
    }
    
    </style>
    """,
    unsafe_allow_html=True
)

# Main Streamlit App
st.markdown('<div class="main-container no-space-top">', unsafe_allow_html=True)
st.markdown('<h1>YouTube Video Summarizer</h1>', unsafe_allow_html=True)
st.markdown('<p>Get concise summaries for any YouTube video instantly.</p>', unsafe_allow_html=True)

youtube_link = st.text_input("Paste YouTube Video URL here...", key="input", placeholder="https://www.youtube.com/watch?v=...")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Summarize", key="button"):
    if youtube_link:
        transcript_text = extract_transcript_details(youtube_link)
        
        if transcript_text:
            summary = generate_gemini_content(transcript_text, prompt)
            st.markdown('<h2>Summary</h2>', unsafe_allow_html=True)
            st.markdown('<div class="summary-box">', unsafe_allow_html=True)
            st.write(summary)
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="powered">Powered by QuadTech❤️ Team</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
