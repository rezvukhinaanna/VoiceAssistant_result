import os, webbrowser, sys, subprocess, pyttsx3, requests
import voice

try:
	import requests
except:
	pass


def browser():
    webbrowser.open('https://www.youtube.com', new=2)


def offpc():
    # команда отключает ПК под управлением Windows

    os.system('shutdown \s')
    print('пк был выключен')


def weather():
    try:
        params = {'q': 'Russia', 'units': 'metric', 'lang': 'ru', 'appid': '86fa644a83e5a7009119e59319606b44'}
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params=params)
        # if not response:
        #    raise
        w = response.json()
        voice.speaker(f"На улице {w['weather'][0]['description']} {round(w['main']['temp'])} градусов")

    except:
        voice.speaker('Произошла ошибка при попытке запроса к ресурсу API, проверь код')


def offBot():
    # отключение бота
    sys.exit()


def passive():
    # функция заглушка при простом диалоге с ботом
    pass