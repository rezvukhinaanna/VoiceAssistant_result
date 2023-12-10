import pyttsx3

# Инициализация голосового "движка" при старте программы
engine = pyttsx3.init()
engine.setProperty('rate', 180)  # Скорость речи

def speaker(text):
    # голос по voice_id
    selected_voice_id = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_RU-RU_IRINA_11.0'
    engine.setProperty('voice', selected_voice_id)

    # Озвучка текста
    engine.say(text)
    engine.runAndWait()
