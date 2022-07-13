from pynput.keyboard import Key, Controller
import time
import os

def type(word, keyboard):
    keyboard.type(word)
    time.sleep(0.5)
    keyboard.press(Key.enter)
    time.sleep(0.5)
    keyboard.release(Key.enter)
    time.sleep(0.5)


input("Ready to type ..... Typing will start after 10s of pressing enter")
time_pass = 0
while time_pass <= 10:
    time.sleep(1)
    time_pass += 1
    if time_pass <= 10:
        print(time_pass)
    else:
        print("Initiating")

keyboard = Controller()
file = open(r"C:\Users\ParadoX\PycharmProjects\Web Crawler v 3.0\New Season Animes\New Animes winter19.txt", "r")
lines = file.readlines()
while True:
    if "\n" in lines:
        lines.pop(lines.index("\n"))
    else:
        break

for line in lines:
    type(line, keyboard)


               
