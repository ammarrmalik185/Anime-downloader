from pynput.keyboard import Key, Controller
import time

season_range = int(input("Enter no of seasons :"))
ep_season = [0]
count = 1
while count <= season_range:
    temp_ep = int(input("Enter number of episodes in season " + str(count) + " :"))
    ep_season.append(temp_ep)
    count += 1

keyboard = Controller()

input("Ready to type ..... Typing will start after 10s of pressing enter")
time_pass = 0
while time_pass <= 10:
    time.sleep(1)
    time_pass += 1
    if time_pass <= 10:
        print(time_pass)
    else:
        print("Initiating")

season = 1
while season <= season_range:
    episode = 1
    while episode <= ep_season[season]:
        text = "S" + str(season) + " e" + str(episode)
        keyboard.type(text)
        keyboard.press(Key.enter)
        time.sleep(0.5)
        keyboard.release(Key.enter)
        time.sleep(0.5)
        episode += 1
    season += 1

input("Process Complete ..... Press Enter to continue ")
