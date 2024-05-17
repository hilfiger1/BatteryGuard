import subprocess
import os
import os.path
import re
import platform
import PySimpleGUI as sg

VACTDISABLED = re.compile(r"VACTDisabled[\s]+0")
encountered_error = False


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


def get_smc_binary_path(script_dir) -> str:
    smc_dir = os.path.join(script_dir, "smc")
    binary_path = os.path.join(smc_dir, "smc")

    if os.path.exists(binary_path):
        return binary_path  # Binary already exists, no need to build

    try:
        with os.scandir(smc_dir):
            pass  # Check if smc_dir exists
    except FileNotFoundError:
        raise FileNotFoundError(f"SMC directory '{smc_dir}' not found")

    try:
        subprocess.check_call(["make"], cwd=smc_dir)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to build SMC binary: {e}")

    if not os.path.exists(binary_path):
        raise FileNotFoundError(f"SMC binary not found at '{binary_path}' after build")

    return binary_path