import time
from datetime import datetime as dt
import os

# Site names to block
sites_to_block = [
    "www.facebook.com",
    "facebook.com",
    "www.youtube.com",
    "youtube.com",
    "www.gmail.com",
    "gmail.com",
]

# Different hosts for different operating systems
Linux_host = "/etc/hosts"
Window_host = r"C:\Windows\System32\drivers\etc\hosts"
default_host = Linux_host if os.name == 'posix' else Window_host

redirect = "127.0.0.1"


def block_websites(start_hour, end_hour):
    while True:
        try:
            current_time = dt.now()
            work_hours = (
                dt(current_time.year, current_time.month, current_time.day, start_hour),
                dt(current_time.year, current_time.month, current_time.day, end_hour),
            )

            if work_hours[0] < current_time < work_hours[1]:
                print("Do the work ....")
                with open(default_host, "r+") as hostfile:
                    hosts = hostfile.read()
                    for site in sites_to_block:
                        if site not in hosts:
                            hostfile.write(redirect + " " + site + "\n")
            else:
                with open(default_host, "r+") as hostfile:
                    hosts = hostfile.readlines()
                    hostfile.seek(0)
                    for host in hosts:
                        if not any(site in host for site in sites_to_block):
                            hostfile.write(host)
                    hostfile.truncate()
                print("Good Time")

            time.sleep(3)

        except PermissionError as e:
            print(f"Caught a permission error: Try running as Admin - {e}")
            # handle the error here or exit the program gracefully
            break


if __name__ == "__main__":
    block_websites(9, 21)
