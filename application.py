import argparse
import os
import subprocess
import sys
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

    def post_exec(self):
        if self.mode:
            Screen.set()

    def execute(self):
        if self.steam_id is None:
            try:
                subprocess.check_call(self.exec_path)
                return True
            except subprocess.CalledProcessError:
                return False
        else:
            return webbrowser.open('steam://rungameid/' + str(self.steam_id))

    def is_running(self):
        process = [item for item in psutil.process_iter() if item.name() == self.process_name]
        return len(process) != 0

    @staticmethod
    def from_string(s):
        try:
            return Application[s]
        except KeyError:
            raise ValueError()


def main(argv=None):
    if argv is None:
        argv = sys.argv

    application = argv['app']
    application.pre_exec()
    if not application.execute():
        Screen.set()
    else:
        time.sleep(application.sleep)   # wait for the app to load
        while application.is_running():
            time.sleep(1)

    application.post_exec()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--app", type=Application.from_string,
                        help="Application name (default: notepad): ".join([app.name for app in Application]),
                        default=Application.NOTEPAD)

    argv = vars(parser.parse_args())

    main(argv)
