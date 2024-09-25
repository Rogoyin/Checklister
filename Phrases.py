import time
import winsound
import tkinter as tk
import random

Phrases = []   


def Window_Phrase ():

    def Random_Phrase():
        return random.choice(Phrases)

    Window = tk.Tk()
    Window.title("")
    Window.geometry("400x200")

    Label_Phrase = tk.Label(Window, text=Random_Phrase(), font=("Arial", 14), wraplength=350, justify="center")
    Label_Phrase.pack(pady=50)

    Window.mainloop()


def Periodic_Phrase(Begin_Hour='08:00', Final_Hour='22:00', Target_Minute=0, Duration_Second=5):
    while True:
        # Obtener la hora actual
        Now = time.localtime()
        Actual_Hour = time.strftime("%H:%M", Now)

        if Begin_Hour <= Actual_Hour < Final_Hour:
            if Now.tm_min == Target_Minute and Now.tm_sec == 0:
                Window_Phrase ()
            time.sleep(1)

        else:
            time.sleep(60)

# Iniciar el programa de frases.
Periodic_Phrase(Target_Minute=0)