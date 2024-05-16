import subprocess
import os
import os.path
import re
import platform
import PySimpleGUI as sg

VACTDISABLED = re.compile(r"VACTDisabled[\s]+0")

def is_system_battery_care_activated() -> bool:
    global encountered_error

    try:
        pmset = subprocess.run(["pmset", "-g"], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        encountered_error = True
        sg.PopupError(f"ERROR: pmset -g command failed: {e}")
        return False
    
    if VACTDISABLED.search(pmset.stdout):
        return True
    return False