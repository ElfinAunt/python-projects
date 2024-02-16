"""
Date: 14-2-24
Day: Wednesday
Project: CountDown GUI Clock
Developer: ElfiAunt
Completed On: 16-2-24
"""
import time, threading
from tkinter import *
import tkinter.ttk as ttk
from pygame import mixer
time_entered = {"Hour": 0, "Minute": 0, "Second": 0}
remove_char = """{}:',"""

def timer_ended(play):
    mixer.init()
    mixer.music.load("timer_ended.mp3")
    mixer.music.play(1)
    while play:
        pass
    mixer.music.stop()
def timer():
    if time_entered["Second"] != 0:
        if time_entered["Minute"] > 0 and time_entered["Second"] == 0:
            time_entered["Second"] = 60
            time_entered["Minute"] -= 1
        if time_entered["Hour"] > 0 and time_entered["Minute"] == 0:
            time_entered["Minute"] = 60
            time_entered["Hour"] -= 1
        time_entered["Second"] -= 1
        time_to_display = str(time_entered)
        for item in remove_char:
            if item == ",":
                time_to_display = time_to_display.replace(item, ":")
            time_to_display = time_to_display.replace(item, "")
        time_label.config(text=str(time_to_display))
        print(time_to_display)
        root.after(1000, timer)
    if time_entered["Second"] == 0:
        time_label.config(text="Countdown Ended")
        threading.Thread(target=timer_ended,args=(1,)).start()


def get_time():
    try:
        time_entered["Hour"] = int(user_input.get().split("-")[0])
        time_entered["Minute"] = int(user_input.get().split("-")[1])
        time_entered["Second"] = int(user_input.get().split("-")[2])+1
        timer()
    except  (IndexError, ValueError):
        time_label.config(text="Wrong Value")
        print("Error In Given Time")


def stop_clock():
    for item in time_entered:
        time_entered[item] = 0
    timer_ended(0)


root = Tk()
root.geometry("700x500")
root.title("CountDown Clock [GUI]")
user_input = StringVar()
style = ttk.Style(root)
style.configure("Padded.TEntry", padding=(180, 0, 20))
time_entry = ttk.Entry(root, textvariable=user_input, font='Helvetica 20 bold', width=10, style="Padded.TEntry")
time_entry.insert(0, " 00-00-00 ")
time_entry.place(rely=0.1, relx=0.5, anchor=CENTER, height=50, width=500)
start_button = Button(root, text="Start-Clock", command=get_time, font='Helvetica 20 bold', bg="cyan")
start_button.place(rely=0.2, relx=0.57, anchor="nw", width=200, height=50)
stop_button = Button(root, text="Stop-Clock", command=stop_clock, font='Helvetica 20 bold', bg="cyan")
stop_button.place(rely=0.2, relx=0.427, anchor="ne", width=200, height=50)
timer_screen = Frame(root, borderwidth="1", relief="solid", width="650", height="300")
timer_screen.place(rely=0.65, relx=0.5, anchor=CENTER)
timer_screen.pack_propagate(0)
time_label = Label(timer_screen, text="Countdown Screen", font='Helvetica 30 bold')
time_label.place(rely=0.5, relx=0.5, anchor=CENTER)
# timer()
root.mainloop()
