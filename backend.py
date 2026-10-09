from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import os

try:
    import google.genai as genai
except ImportError:
    raise ImportError("Please install google-genai")


# -----------------------------
# Load API Key
# -----------------------------
def get_api_key():
    if os.path.exists(".env"):
        with open(".env", "r") as file:
            for line in file:
                if line.startswith("GEMINI_API_KEY="):
                    return line.split("=", 1)[1].strip()

    raise Exception("GEMINI_API_KEY not found in .env")


# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SongRequest(BaseModel):
    theme: str
    story: str
    genre: str


def build_prompt(data):
    return f"""
You are an expert songwriter.

Write an original song using:

Theme:
{data.theme}

Story:
{data.story}

Genre:
{data.genre}

Output exactly in this format:

[TITLE]

[SUGGESTED BPM]

[SUGGESTED KEY]

[CHORD PROGRESSION - VERSES]

[CHORD PROGRESSION - CHORUS]

[VERSE 1]

[CHORUS]

[VERSE 2]

[BRIDGE]

[FINAL CHORUS]

[OUTRO]
"""


@app.get("/")
def home():
    return {"message": "Backend Running!"}


@app.post("/generate")
def generate_song(request: SongRequest):

    client = genai.Client(api_key=get_api_key())

    response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=build_prompt(request)
)

    return {
        "lyrics": response.text
    }