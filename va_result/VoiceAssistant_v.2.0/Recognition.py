import os
import time
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

# Функция для обработки речи с помощью GPT
from GPT import ask_gpt

r = sr.Recognizer()
mic = sr.Microphone(device_index=1)

def record():
    while True:
        mic_status = os.getenv('MIC')
        if mic_status is None:
            mic_status = '0'

        if int(mic_status) == 0:
            break

        print('Rec:')
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            try:
                data = r.recognize_google(audio, language='ru-RU').lower()
            except sr.UnknownValueError:
                data = ''
                pass

        if data != '':
            print(f'You said - {data}')
            answer = ask_gpt(data)
            print(f'Answer - {answer}')
            speak_text(answer)

        # Добавлена задержка перед новой итерацией
        time.sleep(1)

    print('Stop Rec')

def speak_text(text):
    tts = gTTS(text=text, lang='ru')
    tts.save("response1.mp3")
    playsound("response1.mp3")

# Запуск функции записи и обработки речи
record()
