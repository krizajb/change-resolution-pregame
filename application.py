import os
import subprocess
import time
import webbrowser
from enum import Enum
import psutil

from screen import Screen


class Mode(object):

    def __init__(self, width, height, depth, brightness):
        self.width = width
        self.height = height
        self.depth = depth
        self.brightness = brightness


class Application(Enum):
    COUNTER_STRIKE = ("csgo.exe", None, 730, 5, Mode(1920, 1080, 32, 100))
    NOTEPAD = ("notepad.exe", "C:\Windows\System32", None, 1, None)

    def __init__(self, name, exec_path, steam_id, sleep, mode):
        self.process_name = name
        if exec_path:
            exec_path = os.path.join(exec_path, name)
        self.exec_path = exec_path
        self.steam_id = steam_id
        self.sleep = sleep
        self.mode = mode

    def pre_exec(self):
        if self.mode:
            Screen.brightness(self.mode.brightness)
            Screen.set(self.mode.width, self.mode.height, self.mode.depth)

    def execute(self):
        if self.steam_id is None:
            return subprocess.Popen(self.exec_path)
        else:
            return webbrowser.open('steam://rungameid/' + str(self.steam_id))

    def is_running(self):
        process = [item for item in psutil.process_iter() if item.name() == self.process_name]
        return len(process) != 0


if __name__ == '__main__':
    application = Application.NOTEPAD

    application.pre_exec()
    if not application.execute():
        Screen.set()
    else:
        time.sleep(application.sleep)   # wait for the app to load
        while application.is_running():
            time.sleep(1)

    Screen.set()
