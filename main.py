from GUI.control import render_initial, remove_title_frame, pack_canvas_timer_and_button, update_screenshot
from screenshots.simple import grab_save_entire_screen
from notifyers.email import send_report
import os
import tkinter as tk

root = tk.Tk()
current_settings = {}
current_screenshot_path = os.path.join(os.getcwd(), 'current_snapshot.png')


def on_tick():
    grab_save_entire_screen(current_screenshot_path)
    update_screenshot(root, current_screenshot_path)
    send_report(current_settings['email'], 0, current_screenshot_path)


def settings_manager(settings):
    if settings['email'] is not None and settings['period'] is not None:
        remove_title_frame(root)
        global current_settings
        current_settings = settings
        pack_canvas_timer_and_button(root, settings['email'], settings['period'], on_tick)
    return


if __name__ == '__main__':
    root = render_initial(root, settings_manager)
    root.mainloop()
