import datetime
import tkinter as tk
import tkinter.simpledialog as tks
import tkinter.messagebox as tkm
import re
from PIL import ImageTk, Image

schedule = None

def set_basics(root: tk.Tk):
    root.title("IrkTrinket - automated emailed screenshots")
    root.geometry('1024x800')
    #root.attributes('-zoomed', True)
    root.resizable(width=False, height=False)
    return root


def settings_wizard(root: tk.Tk, callback):
    settings = {}
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    email = tks.askstring('Target email', 'Provide a valid email address', parent=root)
    settings['email'] = email
    if email_regex.match(settings['email']):
        period = tks.askinteger('Target period', 'Provide snapshot period in milliseconds')
        settings['period'] = period
        callback(settings)
    else:
        tkm.showerror('Error', 'Not a valid email address.')


def set_menu(root: tk.Tk, settings_callback):
    menu = tk.Menu(root)
    root.config(menu=menu)
    settings = tk.Menu(menu)
    menu.add_cascade(label='Settings', menu=settings)
    settings.add_command(label='Setup', command=lambda: settings_wizard(root, settings_callback))


def set_title_message(root: tk.Tk):
    title_frame = tk.Frame(name='title_frame', master=root, height=300)
    title_frame.pack(fill=tk.X)
    title = tk.Label(
        text="IrkTrinket - send screenshots via email",
        font=("Sans", 16),
        master=title_frame
    )
    title.pack()
    subtitle = tk.Label(
        text="use the setup wizard in the settings menu to enter receiver email and a screenshot period",
        font=("Sans", 12),
        fg="grey",
        wraplength=500,
        master=title_frame
    )
    subtitle.pack()


def remove_title_frame(root: tk.Tk):
    title_frame = root.nametowidget('title_frame')
    if title_frame is not None:
        title_frame.pack_forget()


def pack_canvas_timer_and_button(root: tk.Tk, user_email, user_period, on_tick):
    control_frame = tk.Frame(name='control_frame', master=root)
    control_frame.pack()
    time = datetime.datetime(100, 1, 1, 0, 0, 0)
    timer = tk.Label(
        text=str(time.time()),
        font=("Sans", 14),
        wraplength=500,
        master=control_frame,
        name="progress_timer"
    )
    timer.pack()
    button_start = tk.Button(
        text="Start the automatic screenshots for {}".format(user_email),
        master=control_frame,
        name="progress_start_button",
        command=lambda: ticker(root, timer, time, user_period, on_tick)
    )
    button_cancel = tk.Button(
        text="Stop and reset the automatic screenshots for {}".format(user_email),
        master=control_frame,
        name="progress_stop_button",
        command=lambda: stop_ticker(root, timer)
    )
    button_start.pack()
    button_cancel.pack()
    canvas_frame = tk.Frame(name='canvas_frame', master=root)
    canvas_frame.pack(fill=tk.BOTH)
    canvas = tk.Canvas(name='preview_canvas', master=canvas_frame, height=600, bg="white")
    canvas.pack(fill=tk.BOTH)


def update_screenshot(root: tk.Tk, path):
    canvas = root.nametowidget('canvas_frame.preview_canvas')
    img = ImageTk.PhotoImage(Image.open(path))
    canvas.create_image(0, 0, image=img, anchor=tk.NW)
    canvas.update()


def ticker(root: tk.Tk, timer: tk.Label, time, user_period, on_tick):
    global schedule
    period = user_period
    time = time + datetime.timedelta(milliseconds=period)
    timer.config(text=str(time.time()))
    on_tick()
    schedule = root.after(period, lambda: ticker(root, timer, time, user_period, on_tick))


def stop_ticker(root: tk.Tk, timer: tk.Label):
    global schedule
    root.after_cancel(schedule)
    schedule = None
    timer.config(text=str(datetime.time(0, 0, 0)))


def render_initial(root, settings_callback):
    root = set_basics(root)
    set_menu(root, settings_callback)
    set_title_message(root)
    return root
