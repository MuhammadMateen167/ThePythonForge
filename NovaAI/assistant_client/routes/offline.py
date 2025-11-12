"""
offline.py  —  Handles local (offline) assistant commands.
Safe actions only: information queries and launching known applications.
"""

import os
import platform
import psutil
import shutil
import subprocess
import datetime
from typing import List, Tuple

# -------------------- Command Maps -------------------- #

EXECUTABLES = {
    # Office & text editors
    "word": "winword",
    "excel": "excel",
    "powerpoint": "powerpnt",
    "notepad": "notepad",
    "onenote": "onenote",
    "outlook": "outlook",
    "vscode": "code",
    "codium": "codium",
    "visualstudio": "devenv",
    "pluma": "pluma",
    # Browsers
    "chrome": "chrome",
    "edge": "msedge",
    "firefox": "firefox",
    "safari": "safari",
    "chromium": "chromium",
    # Media & comms
    "vlc": "vlc",
    "spotify": "spotify",
    "teams": "teams",
    "skype": "skype",
    "zoom": "zoom",
    # System utilities
    "calculator": "calc",
    "paint": "mspaint",
    "taskmanager": "taskmgr",
    "explorer": "explorer",
    "cmd": "cmd",
    "terminal": "wt",  # Windows Terminal
}

# -------------------- Helper Functions -------------------- #


def _launch_app(exe: str) -> str:
    """Try to open a known executable cross-platform."""
    system = platform.system().lower()
    try:
        if system == "windows":
            os.system(f"start {exe}")
        elif system == "darwin":  # macOS
            subprocess.run(["open", "-a", exe])
        else:
            subprocess.run([exe])
        return f"Launched {exe}."
    except Exception as e:
        return f"Could not launch {exe}: {e}"


def _open_folder(path: str) -> str:
    """Open a folder with the system’s file explorer."""
    system = platform.system().lower()
    try:
        if system == "windows":
            os.startfile(path)
        elif system == "darwin":
            subprocess.run(["open", path])
        else:
            subprocess.run(["xdg-open", path])
        return f"Opened {path}."
    except Exception as e:
        return f"Failed to open folder: {e}"


# -------------------- Info Utilities -------------------- #


def get_system_info() -> str:
    u = platform.uname()
    return (
        f"System: {u.system}\n"
        f"Node: {u.node}\n"
        f"Release: {u.release}\n"
        f"Version: {u.version}\n"
        f"Machine: {u.machine}\n"
        f"Processor: {u.processor}"
    )


def get_cpu_usage() -> str:
    return f"CPU usage: {psutil.cpu_percent(interval=1)}%."


def get_memory_usage() -> str:
    mem = psutil.virtual_memory()
    return f"RAM used: {mem.percent}% ({mem.used // (1024**3)} GB of {mem.total // (1024**3)} GB)."


def get_disk_usage() -> str:
    d = shutil.disk_usage("/")
    return f"Disk free: {d.free // (1024**3)} GB / {d.total // (1024**3)} GB."


def get_top_processes(limit: int = 5) -> str:
    procs = [
        (p.info["name"], p.info["memory_percent"])
        for p in psutil.process_iter(["name", "memory_percent"])
        if p.info["memory_percent"]
    ]
    procs.sort(key=lambda x: x[1], reverse=True)
    lines = [f"{n} — {m:.2f}% RAM" for n, m in procs[:limit]]
    return "Top processes:\n" + "\n".join(lines)


def get_battery_info() -> str:
    if hasattr(psutil, "sensors_battery"):
        b = psutil.sensors_battery()
        if b:
            return f"Battery: {b.percent}% ({'plugged' if b.power_plugged else 'on battery'})"
    return "Battery information unavailable."


# -------------------- Core Handler -------------------- #


def handle(prompt: str) -> tuple[bool, str]:
    """Main offline dispatcher.
    Returns (handled, reply)
    handled = True if it ran a command, False if it's just a generic fallback
    """
    prompt = prompt.lower().strip()

    # time / date
    if "time" in prompt:
        return True, f"It is {datetime.datetime.now().strftime('%H:%M:%S')}."
    if "date" in prompt:
        return True, f"Today is {datetime.date.today().strftime('%A, %B %d, %Y')}."

    # system information
    if "system info" in prompt or "os info" in prompt:
        return True, get_system_info()
    if "cpu" in prompt:
        return True, get_cpu_usage()
    if "ram" in prompt or "memory" in prompt:
        return True, get_memory_usage()
    if "disk" in prompt:
        return True, get_disk_usage()
    if "process" in prompt:
        return True, get_top_processes()
    if "battery" in prompt:
        return True, get_battery_info()

    # folders
    if "downloads" in prompt:
        return True, _open_folder(os.path.join(os.path.expanduser("~"), "Downloads"))
    if "documents" in prompt:
        return True, _open_folder(os.path.join(os.path.expanduser("~"), "Documents"))
    if "desktop" in prompt:
        return True, _open_folder(os.path.join(os.path.expanduser("~"), "Desktop"))

    # app launches
    if prompt.startswith("open "):
        for key, exe in EXECUTABLES.items():
            if key in prompt:
                return True, _launch_app(exe)
        return True, "I don't know that application yet."

    # generic fallback
    fallback = (
        "I'm offline, but I can show system information, open common apps, "
        "and report usage stats. Try 'open notepad' or 'check memory usage'."
    )
    return False, fallback
