from PIL import ImageGrab


def grab_save_entire_screen(path):
    screenshot = ImageGrab.grab()
    screenshot.save(path)
