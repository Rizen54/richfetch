#!/usr/bin/env python

import os
import psutil
import socket
import typing
import argparse
import platform
import requests
import psutil._common
from termcolor import colored
from cpuinfo import get_cpu_info
from datetime import datetime, timedelta


def get_public_ip() -> str | None:
    """
    Retrieves the public IP address of the current machine using the ipify API.

    This function sends a request to the ipify service to obtain the public IP address.
    If the request is successful, it returns the IP address as a string. If an error
    occurs during the request (e.g., network issues or server errors), it logs the error
    and returns None.

    Returns:
        str | None: The public IP address as a string if the request is successful,
                    or None if an error occurs.
    """
    try:
        response: requests.Response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        return response.json()["ip"]
    except requests.exceptions.RequestException as e:
        # Handle specific request exceptions (e.g., network errors)
        print(f"Error retrieving public IP address: {e}")
        return None
    except Exception as e:
        # Catch any other unexpected exceptions
        print(f"Unexpected error: {e}")
        return None


def get_private_ip() -> str | None:
    """
    Retrieves the private IP address of the current machine.

    This function creates a temporary UDP socket to determine the local IP address
    by connecting to a well-known public IP (Google's DNS server, 8.8.8.8). It does not
    send any data to the server; the operation is used only to get the local IP address
    assigned to the network interface.

    If the operation is successful, it returns the local IP address as a string. If an
    error occurs during the socket operation, it logs the error and returns None.

    Returns:
        str | None: The private IP address as a string if the operation is successful,
                    or None if an error occurs.
    """
    try:
        s: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip: str = s.getsockname()[0]
        s.close()
        return ip
    except socket.error as e:
        # Handle socket-specific errors
        print(f"Error retrieving local IP address: {e}")
        return None
    except Exception as e:
        # Catch any other unexpected exceptions
        print(f"Unexpected error: {e}")
        return None


def get_cpu_temperature() -> float | None:
    """
    Retrieves the current CPU temperature from available sensors.

    This function attempts to get the CPU temperature using several known sensor names.
    It is designed to work on Linux or FreeBSD-based operating systems where the
    `psutil.sensors_temperatures()` function can read sensor data.

    The function iterates through a list of common sensor names, checking each one until
    it finds a sensor with a temperature reading. If a sensor is found, it returns the
    current temperature as a float. If no sensor is found or if an error occurs, it
    returns None.

    Returns:
        float | None: The current CPU temperature if a sensor reading is found,
                            or None if no sensor reading is available.
    """
    sensors: list[str] = [
        "coretemp",
        "k10temp",
        "cpu-thermal",
        "lm_sensors",
        "asus-nb",
        "lm75",
        "acpitz",
    ]

    all_temperatures: dict[str, psutil.shwtemp] = psutil.sensors_temperatures()
    if all_temperatures is None:
        return None

    for sensor in sensors:
        temperatures = all_temperatures.get(sensor)
        if temperatures:
            return temperatures[0].current

    return None


def color_cpu_temp(temp: float) -> str:
    """
    Determines the color label for the CPU temperature based on its value.

    This function returns a color code depending on the CPU temperature:
    - "green" for temperatures below 60 degrees.
    - "yellow" for temperatures between 60 and 69 degrees.
    - "red" for temperatures of 70 degrees or higher.

    Args:
        temp (float): The current CPU temperature.

    Returns:
        str: The color label ("green", "yellow", or "red") representing the temperature level.
    """
    if temp < 60:
        return "green"
    elif temp < 70:
        return "yellow"
    else:
        return "red"


def color_usage_percent(percent: float) -> str:
    """
    Determines the color label for the CPU usage percentage based on its value.

    This function returns a color code depending on the CPU usage percentage:
    - "green" for usage below 60%.
    - "yellow" for usage between 60% and 79%.
    - "red" for usage of 80% or higher.

    Args:
        percent (float): The CPU usage percentage.

    Returns:
        str: The color label ("green", "yellow", or "red") representing the usage level.
    """
    if percent < 60:
        return "green"
    elif percent < 80:
        return "yellow"
    else:
        return "red"


def get_os_logo(os_name: str) -> str:
    """
    Returns the corresponding logo icon for a given operating system name.

    This function uses a dictionary to map operating system names to their respective
    logo icons, with the icon colored using the `colored` function.

    If the specified operating system name is not found in the dictionary, a default icon
    is returned.

    Args:
        os_name (str): The name of the operating system.

    Returns:
        str: The logo icon for the specified operating system, with color formatting applied.
    """
    logo_dict: dict[str, str] = {
        "Alpine Linux": colored("", "blue"),
        "Arch Linux": colored("󰣇", "blue"),
        "Artix Linux": colored("", "blue"),
        "CentOS Stream 9": colored("", "yellow"),
        "Debian GNU/Linux 11 Bullseye": colored("", "red"),
        "Deepin": colored("", "blue"),
        "Elementary OS 7: Loki": colored("", "blue"),
        "EndeavourOS": colored("", "magenta"),
        "Fedora Linux": colored("", "blue"),
        "FreeBSD": colored("", "red"),
        "Parabola GNU/Linux-libre": colored("", "blue"),
        "Garuda Linux": colored("", "yellow"),
        "Gentoo Linux": colored("󰣨", "white"),
        "Hyperbola GNU/Linux-libre": colored("", "blue"),
        "Kali Linux": colored("", "blue"),
        "KDE Neon": colored("", "blue"),
        "Kubuntu": colored("", "blue"),
        "Linux Mint 21 Cinnamon": colored("󰣭", "green"),
        "Lubuntu": colored("", "blue"),
        "macOS": colored("", "white"),
        "Mageia": colored("", "blue"),
        "Manjaro Linux": colored("", "green"),
        "MX Linux": colored("", "white"),
        "NixOS": colored("", "blue"),
        "openSUSE Leap 15.4": colored("", "green"),
        "openSUSE Tumbleweed": colored("", "green"),
        "Parrot Security OS": colored("", "green"),
        "Pop!_OS 22.04": colored("", "blue"),
        "PostmarketOS": colored("", "green"),
        "Puppy Linux": colored("", "white"),
        "Qubes OS": colored("", "blue"),
        "Raspberry Pi OS": colored("", "red"),
        "Red Hat Enterprise Linux": colored("Red Hat Enterprise Linux", "red"),
        "Slackware Linux": colored("", "blue"),
        "Solus": colored("", "blue"),
        "Tails": colored("", "magenta"),
        "Ubuntu 22.04 LTS": colored("", "yellow"),
        "Ubuntu Budgie": colored("", "magenta"),
        "Vanilla OS": colored("", "yellow"),
        "Void Linux": colored("", "green"),
        "Windows": colored("", "blue"),
        "Xubuntu": colored("", "blue"),
        "Zorin OS": colored("", "blue"),
    }

    return logo_dict.get(os_name, colored("", "yellow"))


def color_line() -> str:
    """
    Creates a colored line of symbols using predefined colors.

    This function constructs a string consisting of colored symbols,
    where each symbol is colored using the `colored` function. The
    symbols used are the same for each color.

    Returns:
        str: A string containing colored symbols in a single line.
    """
    colors: list[str] = ["red", "yellow", "green", "blue", "cyan", "magenta"]
    colored_line: str = " ".join(colored(" ", color) for color in colors)
    return colored_line


def dynamic_color_line() -> str:
    """
    Creates a dynamically colored line of symbols.

    This function constructs a string consisting of colored symbols,
    where each symbol is associated with a corresponding color from
    two predefined lists. Each symbol is colored using the `colored`
    function.

    Returns:
        str: A string containing dynamically colored symbols in a single line.
    """
    colors: list[str] = ["red", "yellow", "green", "blue", "cyan", "magenta"]
    symbols: list[str] = ["󱚝", "󱚟", "󱚣", "󰚩", "󱜙", "󱚥"]

    colored_line: str = " ".join(
        colored(symbols[i], colors[i]) for i in range(len(colors))
    )
    return colored_line


def get_system_info() -> dict[str, typing.Any]:
    """
    Retrieves system information including OS details, username, uptime,
    CPU information, memory usage, disk space, and IP addresses.

    This function uses various system libraries to gather information about
    the system and returns it in a structured dictionary format.

    Returns:
        dict[str, typing.Any]: A dictionary containing system information.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="RichFetch - A customizable system information tool"
    )
    parser.add_argument(
        "--show-public-ip", action="store_true", help="Show public IP address"
    )
    parser.add_argument(
        "--show-private-ip", action="store_true", help="Show private IP address"
    )
    args: argparse.Namespace = parser.parse_args()

    # OS name and version
    os_type: str = platform.system()
    os_name: str
    os_logo: str

    if os_type == "Darwin":
        version = platform.mac_ver()[0]
        os_name = f"macOS {version}"
        os_logo = get_os_logo("macOS")
    elif os_type == "Windows":
        version = platform.win32_ver()
        os_name = f"Windows {version}"
        os_logo = get_os_logo("Windows")
    else:
        os_name = platform.freedesktop_os_release()["PRETTY_NAME"]
        os_logo = get_os_logo(os_name)

    # Username and hostname
    username: str = os.getlogin()
    hostname: str = os.uname().nodename

    # Uptime calculation
    uptime_seconds: float = psutil.boot_time()
    current_time: datetime = datetime.now()
    boot_time: timedelta = current_time - datetime.fromtimestamp(uptime_seconds)
    uptime_str: str = (
        f"{int(boot_time.total_seconds() // 3600)} hrs, {int((boot_time.total_seconds() % 3600) // 60)} mins"
    )

    # Window Manager (WM)
    wm: str | None = os.environ.get("DESKTOP_SESSION") or os.environ.get(
        "XDG_SESSION_TYPE"
    )

    # CPU information
    cpu_info: dict[str, str] = get_cpu_info()
    cpu_name: str = cpu_info["brand_raw"]
    cpu_per: float = psutil.cpu_percent()
    cpu_usage_color: str = color_usage_percent(cpu_per)

    # Fetching CPU temperature
    temp: float = get_cpu_temperature()
    temp_str: str | None = f"{temp}󰔄" if temp is not None else None
    temp_color: str | None = color_cpu_temp(temp) if temp is not None else "red"

    # Battery status
    battery: psutil._common.sbattery = psutil.sensors_battery()
    battery_percent: str | None = f"{round(battery.percent)}%" if battery else None
    plugged: bool | None = battery.power_plugged if battery else None
    battery_logo: str = "󰂄" if plugged else "󱊣"

    # Getting IP addresses
    private_ip: str | None = get_private_ip() if args.show_private_ip else None
    public_ip: str | None = get_public_ip() if args.show_public_ip else None

    # Disk space
    disk_usage: psutil._common.sdiskusage = psutil.disk_usage("/")
    disk_usage_str: str = (
        f"{disk_usage.used / (1024**3):.2f} / {disk_usage.total / (1024**3):.2f} GB ({disk_usage.percent:.2f}%)"
    )
    disk_usage_color: str = color_usage_percent(disk_usage.percent)

    # RAM space
    ram_usage: psutil._pslinux.svmem = psutil.virtual_memory()
    ram_usage_str: str = (
        f"{ram_usage.used / (1024**3):.2f} / {ram_usage.total / (1024**3):.2f} GB ({ram_usage.percent:.2f}%)"
    )
    ram_usage_color: str = color_usage_percent(ram_usage.percent)

    # Colors
    colored_line: str = dynamic_color_line()

    # Display dictionary
    display: dict[str, typing.Any] = {
        colored("", "green"): colored(f"{username}@{hostname}", "green"),
        os_logo: os_name,
        colored("", "blue"): cpu_name,
        colored("", cpu_usage_color): f"{cpu_per}%",
        **({colored("", temp_color): temp_str} if temp_str else {}),
        **(
            {colored(battery_logo, "green"): battery_percent} if battery_percent else {}
        ),
        colored("󰨇", "red"): wm,
        colored("", "magenta"): uptime_str,
        colored("", ram_usage_color): ram_usage_str,
        colored("", disk_usage_color): disk_usage_str,
        **({colored("󰩩", "green"): private_ip} if private_ip else {}),
        **({colored("󰑩", "green"): public_ip} if public_ip else {}),
        " ": colored_line,
    }

    return display


def main() -> None:
    """
    Main function to retrieve and display system information.

    This function calls `get_system_info` to retrieve system information
    and then prints it in a formatted manner.
    """
    system_info: dict[str, typing.Any] = get_system_info()

    print(
        "\n"
        + "\n".join(f"  {key}  {value}" for key, value in system_info.items())
        + "\n"
    )


if __name__ == "__main__":
    main()
