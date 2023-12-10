import os
import sys
import tkinter as tk
from tkinter import ttk
from threading import Thread

from PIL import Image, ImageTk

from Recognition import record


class Application(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.overrideredirect(True)
        self.resizable(False, False)
        self.prepare_img()
        self.create_widgets()
        self.update()

        self.geometry('+{}+{}'.format(self.winfo_screenwidth() - self.winfo_width(),
                                      self.winfo_screenheight() - 100))

        # запуск прослушки микрофона(аппаратной части ассистента)
        # self.run_assistant()
        # запуск функции постоянной проверки значения переменной окружения
        # для обновления виджета, если есть активный диалог с gpt
        #self.check_env_vars()

    def create_widgets(self):
        self.assistant_label = ttk.Label(self, image=self.assistant_img_frames[0], background='black')
        self.assistant_label.grid(column=0, row=0, ipadx=0, ipady=0, padx=0, pady=0)
        self.assistant_label.bind("<Button-1>", self.run_assistant)

        self.exit_label = ttk.Label(self, image=self.exit_img, background='black')
        self.exit_label.grid(column=3, row=0, ipadx=0, ipady=0, padx=0, pady=0)
        self.exit_label.bind("<Button-1>", self.exit)

    def read_gif_frames(self, gif):
        frames = []
        for frame in range(0, gif.n_frames):
            gif.seek(frame)
            frames.append(ImageTk.PhotoImage(gif.copy()))
        return frames

    def prepare_img(self):
        image = Image.open("images/mic.gif")
        self.assistant_img_frames = self.read_gif_frames(image)

        self.exit_img = tk.PhotoImage(file="images/exit.png")


    def animate_mic(self, frame_index=0):
        self.assistant_label.configure(image=self.assistant_img_frames[frame_index])
        self.wheel_mic_animation = self.after(100, self.animate_mic,
                                              (frame_index + 1) % len(self.assistant_img_frames))

    def stop_mic_animation(self):
        if self.wheel_mic_animation is not None:
            self.after_cancel(self.wheel_mic_animation)
            self.wheel_mic_animation = None

    def run_assistant(self, event=None):
        if int(os.getenv('MIC')):

            os.environ.update(MIC='0')
            self.stop_mic_animation()
            self.assistant_label['image'] = self.assistant_img_frames[0]

        else:
            os.environ.update(MIC='1')
            self.animate_mic()
            p1 = Thread(target=record, daemon=True)
            p1.start()

    def exit(self, event):
        sys.exit(0)