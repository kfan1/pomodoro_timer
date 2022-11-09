import math
from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
check_mark = []
timer = None


# ---------------------------- TIMER RESET ------------------------------- #
def pause():
    global reps
    global timer
    global WORK_MIN
    global SHORT_BREAK_MIN
    global LONG_BREAK_MIN
    times = canvas.itemcget(timer_text, 'text').split(':')
    WORK_MIN = int(times[0]) + (int(times[1]) / 60)
    SHORT_BREAK_MIN = int(times[0]) + (int(times[1]) / 60)
    LONG_BREAK_MIN = int(times[0]) + (int(times[1]) / 60)
    reps -= 1
    window.after_cancel(timer)
    start_button.config(text='Start', command=start)


def reset():
    global timer
    global check_mark
    global reps
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="0:00")
    for i in range(reps - 1):
        check_mark[int(i / 2)].destroy()
    reps = 0
    check_mark = []
    text.config(text='Timer', foreground=GREEN)
    start_button.config(text='Start', command=start)


# ---------------------------- TIMER MECHANISM ------------------------------- # 

def start():
    global reps
    global check_mark
    reps += 1
    start_button.config(text='Stop', command=pause)
    if reps > 8:
        return
    if reps == 8:
        check_mark.append(Label(text='✔', background=YELLOW, foreground=GREEN, font=(FONT_NAME, 15, 'bold')))
        check_mark[int(reps / 2 - 1)].place(relx=0.3 + (reps / 30), rely=0.8)
        text.config(text='Break', foreground=GREEN)
        seconds_countdown(LONG_BREAK_MIN * 60)
    elif reps % 2 == 1:
        text.config(text='Work', foreground=RED)
        seconds_countdown(WORK_MIN * 60)
    elif reps % 2 == 0:
        check_mark.append(Label(text='✔', background=YELLOW, foreground=GREEN, font=(FONT_NAME, 15, 'bold')))
        check_mark[int(reps / 2 - 1)].place(relx=0.3 + (reps / 30), rely=0.8)
        text.config(text='Break', foreground=PINK)
        seconds_countdown(SHORT_BREAK_MIN * 60)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def seconds_countdown(seconds):
    global timer
    global WORK_MIN
    global SHORT_BREAK_MIN
    global LONG_BREAK_MIN
    minutes = math.floor(seconds / 60)
    seconds1 = "{:02d}".format(
        int(seconds % 60))                                          ##### Dynamic typing is the ability to change the variable type when reassigning a variable
    canvas.itemconfig(timer_text, text=f"{minutes}:{seconds1}")     ##### only available in python
    if seconds > 0:
        timer = window.after(1000, seconds_countdown, seconds - 1)
    else:
        LONG_BREAK_MIN = 20
        SHORT_BREAK_MIN = 5
        WORK_MIN = 25
        start()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Pomodoro')

canvas = Canvas(background=YELLOW, height=400, width=400)
tomato = PhotoImage(file='tomato.png')
canvas.create_image(200, 200, image=tomato)
timer_text = canvas.create_text(200, 220, text='0:00', font=(FONT_NAME, 28, 'bold'), fill='white')

text = Label(text='Timer', font=(FONT_NAME, 40, 'bold'), background=YELLOW, foreground=GREEN)

start_button = Button(text='Start', width=5, command=start)
stop_button = Button(text='Reset', width=5, command=reset)

canvas.pack()
text.place(relx=0.33, rely=0.05)
start_button.place(relx=0.2, rely=0.8)
stop_button.place(relx=0.7, rely=0.8)

window.mainloop()
