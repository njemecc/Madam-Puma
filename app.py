from openai import OpenAI
import speech_recognition as sr
import pygame
import time
from dotenv import load_dotenv
import os


def record_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say something...")
        audio_data = recognizer.listen(source)
        print("Recording complete.")
        with open(file_path, "wb") as audio_file:
            audio_file.write(audio_data.get_wav_data())

def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    # Wait until the audio is finished playing
    while pygame.mixer.music.get_busy():
        time.sleep(1)


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

  response.stream_to_file('output.mp3')
  play_audio('output.mp3')
