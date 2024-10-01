#!/usr/bin/env python
from cpuinfo import get_cpu_info
import ctypes
from termcolor import colored
import os
import psutil
import subprocess
import socket
import requests
from datetime import datetime
from platform import freedesktop_os_release


def get_public_address():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        return response.json()["ip"]
    except Exception:
        return None


def get_local_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return None


def get_cpu_temperature():
    # Gets CPU temp but only works in Linux or FreeBSD based OS
    
    sensors = ["coretemp", "k10temp", "cpu-thermal", "cpu-thermal", "lm_sensors" "asus-nb", "lm75", "acpitz"]

    for sensor in sensors:
        try:
            temperatures = psutil.sensors_temperatures()[sensor]
            if temperatures:
                return temperatures[0].current
                break  # Exit the inner loop if a matching reading is found
        except (KeyError, IndexError):
            pass

    return None


def color_cpu_temp(temp):
    # Deciding color of cpu temp label depending on the temp
    if temp < 60:
        return "green"
    elif temp >= 60 and temp < 70:
        return "yellow"
    elif temp >= 70:
        return "red"


def color_usage_percent(percent):
    # Deciding color of cpu temp label depending on the temp
    if percent < 60:
        return "green"
    elif percent >= 60 and percent < 80:
        return "yellow"
    elif percent >= 80:
        return "red"


def get_os_logo(os_name):
    logo_dict = {
        "Alpine Linux": colored('', 'blue'),
        "macOS": colored('', 'white'),
        "Arch Linux": colored('󰣇', 'blue'),
        "Artix Linux": colored('', 'blue'),
        "CentOS Stream 9": colored('', 'yellow'),
        "Debian GNU/Linux 11 Bullseye": colored('', 'red'),
        "Deepin": colored('', 'blue'),
        "Elementary OS 7: Loki": colored('', 'blue'),
        "EndeavourOS": colored('', 'magenta'),
        "Fedora Linux": colored('', 'blue'),
        "FreeBSD": colored('', 'red'),
        "Parabola GNU/Linux-libre": colored('', 'blue'),
        "Garuda Linux": colored('', 'yellow'),
        "Gentoo Linux": colored('󰣨', 'white'),
        "Hyperbola GNU/Linux-libre": colored('', 'blue'),
        "Kali Linux": colored('', 'blue'),
        "KDE Neon": colored('', 'blue'),
        "Kubuntu": colored('', 'blue'),
        "Linux Mint 21 Cinnamon": colored('󰣭', 'green'),
        "Lubuntu": colored('', 'blue'),
        "Mageia": colored('', 'blue'),
        "Manjaro Linux": colored('', 'green'),
        "MX Linux": colored('', 'white'),
        "NixOS": colored('', 'blue'),
        "openSUSE Leap 15.4": colored('', 'green'),
        "openSUSE Tumbleweed": colored('', 'green'),
        "Parabola GNU/Linux-libre": colored('', 'blue'),
        "Parrot Security OS": colored('', 'green'),
        "Pop!_OS 22.04": colored('', 'blue'),
        "PostmarketOS": colored('', 'green'),
        "Puppy Linux": colored('', 'white'),
        "Qubes OS": colored('', 'blue'),
        "Raspberry Pi OS": colored('', 'red'),
        "Red Hat Enterprise Linux": colored('Red Hat Enterprise Linux', 'red'),
        "Slackware Linux": colored('', 'blue'),
        "Solus": colored('', 'blue'),
        "Tails": colored('', 'magenta'),
        "Ubuntu 22.04 LTS": colored('', 'yellow'),
        "Ubuntu Budgie": colored('', 'magenta'),
        "Vanilla OS":  colored('', 'yellow'),
        "Void Linux": colored('', 'green'),
        "Windows": colored('', 'blue'),
        "Xubuntu": colored('', 'blue'),
        "Zorin OS": colored('', 'blue'),
    }

    if os_name in logo_dict:
        return logo_dict[os_name]
    else:
        return colored('', 'yellow')


def color_line():
    colors = ["red", "yellow", "green", "blue", "cyan", "magenta"]
    colored_line = ""
    for color in colors:
        colored_line += colored(" ", color)
    return colored_line


def dynamic_color_line():
    colors = ["red", "yellow", "green", "blue", "cyan", "magenta"]
    symbols = ["󱚝", "󱚟", "󱚣", "󰚩", "󱜙", "󱚥"]

    colored_line = ""
    for i in range(len(colors)):
        colored_symbol = colored(symbols[i], colors[i])
        colored_line += colored_symbol + " "
    return colored_line 


def get_system_info():
    # OS name and ver
    os_name = freedesktop_os_release()["PRETTY_NAME"]
    os_logo = get_os_logo(os_name)

    # Username and hostname
    username = os.getlogin()
    hostname = os.uname().nodename

    # Uptime
    uptime_seconds = psutil.boot_time()
    current_time = datetime.now()
    boot_time = current_time - datetime.fromtimestamp(uptime_seconds)

    # Calculate uptime in hours and minutes
    uptime_hours = int(boot_time.total_seconds() // 3600)
    uptime_minutes = int((boot_time.total_seconds() % 3600) // 60)
    uptime_str = f"{uptime_hours} hrs, {uptime_minutes} mins"

    # Window Manager (WM)
    wm = os.environ.get("DESKTOP_SESSION") or os.environ.get("XDG_SESSION_TYPE")

    # CPU name
    cpu_info = get_cpu_info()
    cpu_name = cpu_info["brand_raw"]
    cpu_per = psutil.cpu_percent()
    cpu_usage_color = color_usage_percent(cpu_per)

    # Fetching temp
    temp = get_cpu_temperature()

    if temp is not None:
        temp_str = f"{temp}󰔄"
        temp_color = color_cpu_temp(temp)
    else:
        temp_str = "CPU Temp not found. You're either on Windows or CPU sensors unrecognized."
        temp_color = "red"
    
    # Getting ip addresses
    # local_address = get_local_address()
    # public_address = get_public_address()

    # Disk space
    disk_usage = psutil.disk_usage("/")
    disk_total = disk_usage.total / (1024 ** 3)
    disk_used = disk_usage.used / (1024 ** 3)
    disk_usage_str = f"{disk_used:.2f} / {disk_total:.2f} GB ({disk_usage.percent:.2f}%)"
    disk_usage_color = color_usage_percent(disk_usage.percent)

    # RAM space
    ram_usage = psutil.virtual_memory()
    ram_total = ram_usage.total / (1024 ** 3)
    ram_used = ram_usage.used / (1024 ** 3)
    ram_usage_str = f"{ram_used:.2f} / {ram_total:.2f} GB ({ram_usage.percent:.2f}%)"
    ram_usage_color = color_usage_percent(ram_usage.percent)

    # Colors
    colored_line = dynamic_color_line()


    return {
        colored("", "green"): colored(f"{username}@{hostname}", "green"),
        os_logo: os_name,
        colored("", "blue"): cpu_name,
        colored("", cpu_usage_color): f"{cpu_per}%",
        colored("", temp_color): temp_str,
        colored("󰨇", "red"): wm,
        colored("", "magenta"): uptime_str,
        colored("", ram_usage_color): ram_usage_str,
        colored("", disk_usage_color): disk_usage_str,
        # colored("󰩩", "yellow"): local_address,
        # colored("󰩩", "green"): public_address,
        " ": colored_line,
    }


if __name__ == "__main__":

    system_info = get_system_info()

    print("\n", end="")
    for key, value in system_info.items():
        print(f"  {key}  {value}")
