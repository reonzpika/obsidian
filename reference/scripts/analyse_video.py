"""
Analyse a YouTube video using Gemini 2.5 Flash.
Usage: python analyse_video.py <youtube_url>
Requires: GEMINI_API_KEY environment variable
"""

import os
import sys
from google import genai
from google.genai import types

PROMPT = """
Analyse this video thoroughly. I want to understand both what is SAID and what is SHOWN visually.

Please provide:

1. TRANSCRIPT SUMMARY
   - Key points made verbally, in order
   - Direct quotes for any important statements

2. VISUAL ANALYSIS
   - What is shown on screen (slides, demos, diagrams, text overlays, UI)
   - Any visual content that adds meaning not captured in speech
   - Timestamps or sequence where relevant

3. CORE ARGUMENT / THESIS
   - What is the central idea or message of this video?

4. KEY TAKEAWAYS
   - 5-7 bullet points a reader should walk away with

5. QUESTIONS RAISED
   - Any claims that need verification or follow-up

Be specific. Do not pad. Use bullet points.
"""

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY environment variable not set.")
        sys.exit(1)

    url = sys.argv[1] if len(sys.argv) > 1 else "https://youtu.be/UHVFcUzAGlM"

    client = genai.Client(api_key=api_key)

    print(f"Sending to Gemini 2.5 Flash: {url}")
    print("Analysing... (may take 15-30 seconds)\n")

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part(
                file_data=types.FileData(file_uri=url)
            ),
            types.Part(text=PROMPT),
        ],
    )

    print(response.text)

if __name__ == "__main__":
    main()
