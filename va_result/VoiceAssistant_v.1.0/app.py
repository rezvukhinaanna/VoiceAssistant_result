import queue
import sounddevice as sd  # позволяет получить доступ к аудиоданным с микрофона
import vosk
import json
import words
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from skills import *
import voice

q = queue.Queue()

model = vosk.Model('vosk_model_small')

device = sd.default.device = 1, 3
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])  # получаем частоту микрофона


def callback(indata, frames, time, status):

    q.put(bytes(indata))

def recognize(data, vectorizer,clf):  # анализ распознанного текста
    trg = words.TRIGGERS.intersection(data.split())
    if not trg:
        return

    # удаляем имя бота из текста
    data.replace(list(trg)[0], '')

    # получаем вектор полученного текста
    # сравниваем с вариантами, получая наиболее подходящий ответ
    text_vector = vectorizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]

    # получение имени функции из ответа из data_set
    func_name = answer.split()[0]

    # озвучка ответа из модели data_set
    voice.speaker(answer.replace(func_name, ''))

    # запуск функции из skills
    exec(func_name + '()')

def main():

    # Обучение матрицы на data_set модели
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))  # преобразование текста в матрицу чисел

    clf = LogisticRegression()  # объект для классификации текстовых данных
    clf.fit(vectors, list(words.data_set.values()))  # обучение ии на матрице и соотвествующих слов из words

    # del words.data_set

    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device[0],
                           dtype="int16", channels=1, callback=callback):  # получение аудиосигнала с микрофона

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                recognize(data, vectorizer, clf)

if __name__ == '__main__':
    main()