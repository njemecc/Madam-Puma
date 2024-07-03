from openai import OpenAI
import speech_recognition as sr
from dotenv import load_dotenv
import os
from utils import record_audio
from utils import play_audio

load_dotenv()
api_key = os.getenv("OPENAI_SECRET_KEY")

client = OpenAI(api_key = api_key)

while True:
  record_audio('test.wav')
  audio_file= open('test.wav', "rb")
  transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
  )

  print(transcription.text)

  response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
      {"role": "system", "content": "You are chat gpt. Please answer in short sentences."},
      {"role": "user", "content": f"Please answer: {transcription.text}"},
    ]
  )

  print(response.choices[0].message.content)

 

  response = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input=response.choices[0].message.content
  )

  if os.path.exists("output.mp3"):
            os.remove("output.mp3")

  response.stream_to_file('output.mp3')
  play_audio('output.mp3')
