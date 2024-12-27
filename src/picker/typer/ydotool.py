import os
import subprocess as sp
from subprocess import run

from ..abstractionhelper import get_event_code, is_installed
from ..action import __get_codepoints as get_codepoints
from .typer import Typer

class YdotoolTyper(Typer):
    def __init__(self):
        super().__init__()
        
        self.socket = "/run/user/1000/.ydotool_socket"
        if "YDOTOOL_SOCKET" in os.environ:
            self.socket = os.environ["YDOTOOL_SOCKET"]
        
    @staticmethod
    def name():
        return "ydotool"
    
    @staticmethod
    def supported():
        try:
            return is_installed("ydotool")
        except sp.CalledProcessError:
            return False
    
    def get_active_window(self):
        return "not possible with ydotool"
    
    def type_characters(self, characters: str, active_window: str) -> None:
        # characters is assumed to be a string of emojis; for each emoji,
        # get the unicode code point, then for each char in the unicode code point,
        # get the event code for the char, then send the event code to ydotool
        for character in characters:
            # Get the unicode code point for the emoji
            unicode_code_point = get_codepoints(character)

            # Get keypresses for Ctrl, Shift, U, and the unicode code point
            Ctrl = get_event_code("LeftCtrl")
            Shift = get_event_code("LeftShift")
            U = get_event_code("U")
            Ctrl_release = get_event_code("LeftCtrl", False)
            Shift_release = get_event_code("LeftShift", False)
            U_release = get_event_code("U", False)
            points = []
            
            for point in unicode_code_point:
                points.append(get_event_code(point))
                points.append(get_event_code(point, False))

            # Send the event codes to ydotool
            the_array = ["ydotool", "key", "--key-delay", "1", Ctrl, Shift, U, U_release] + points + [Shift_release, Ctrl_release]
            run(the_array, env=os.environ.copy().update({"YDOTOOL_SOCKET": self.socket}))

    def insert_from_clipboard(self, active_window: str) -> None:
        Shift = get_event_code("LeftShift")
        Shift_release = get_event_code("LeftShift", False)
        Insert = get_event_code("Insert")
        Insert_release = get_event_code("Insert", False)
        
        run(["ydotool", "key", Shift, Insert, Insert_release, Shift_release], 
            env=os.environ.copy().update({"YDOTOOL_SOCKET": self.socket}))
