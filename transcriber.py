import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def transcribe_audio(audio_file) -> str:
    """Transcribes uploaded classroom audio (.mp3, .wav, .m4a, etc.) using Groq Whisper."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing. Please add it to your .env file.")

    client = Groq(api_key=api_key)

    filename = audio_file.name if hasattr(audio_file, "name") else "lecture.mp3"
    file_bytes = audio_file.getvalue() if hasattr(audio_file, "getvalue") else audio_file

    transcription = client.audio.transcriptions.create(
        file=(filename, file_bytes),
        model="whisper-large-v3-turbo",
        response_format="text",
    )
    return str(transcription).strip()