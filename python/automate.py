
# Native Packages
import os, subprocess, sys, asyncio
from threading import Thread

# Additional Dependencies
from termcolor import colored, cprint
import pyperclip

# Automation Packages
import pyautogui as py
import pygetwindow as pw

# package
from timings import delay
from emoji import sad, happy
from errors import InvalidVariables
from data import bootArchive

# Overwatch Window
window: pw.Window = None
_typing_delay = delay.get("typing")
_animation_delay = delay.get("animation")


# default codex
__invalid__description = "Whoops.. Import Error D:"
__default__code = "settings{main{Description: \"" + __invalid__description +"\"}modes{Practice Range}}"

_dataManager = None


# Start Overwatch
async def overwatch():

    print("Attempting to launch " + colored("Overwatch", "yellow", attrs=["bold"]))

    try:
        os.startfile(os.getenv("OVERWATCH_PATH"))

    except FileNotFoundError as error:
        print()
        print(f'    { sad() } { colored("File Not Found", "red", attrs=["bold", "blink"]) }')
        print(f'\t• { colored(error.filename, "red") } was not found')
        sys.exit()

    # Starting Message
    print()
    cprint("Starting", "yellow", attrs=["bold"])
    print(f'{ happy() }: Starting overwatch..')

    await waitForWindow()


# Quit Overwatch (if open)
async def quitOverwatch():

    try:
        subprocess.check_call("taskkill /f /im Overwatch.exe", stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        print(f'Quit { colored("Overwatch", "yellow", attrs=["bold"]) } { colored("(was running)", "magenta") }')

    except:
        return


# waits for an open overwatch window
async def waitForWindow():

    # new window
    global window

    while not bool(window):
    
        if "Overwatch" not in pw.getAllTitles():
            await asyncio.sleep(delay["interval"])
            continue

        else:
            window = pw.getWindowsWithTitle("Overwatch")[0]

    # dimensions: [[ratio x, ratio y], scale]
    dimensions = [[16, 9], 40]

    # optional config variable "window"
    # format: [16:9, 20] (ratio, scale)
    if os.getenv('window'):
        try:
            dimensions = os.getenv('window').replace('[', '').replace(']', '').split(', ')
            dimensions = [[float(dimensions[0].split(':')[0]), float(dimensions[0].split(':')[1])], float(dimensions[1])]

        except:
            cprint("\nwindow config variable must follow this format:\n[16:9, 40] (example for a 16:9 window with 40px scale)", "red")
            raise InvalidVariables

    # window dimensions
    scalar = dimensions[1]
    ratio = {
        "x": dimensions[0][0],
        "y": dimensions[0][1],
    }

    # pixel sizes
    x = int(ratio.get("x") * scalar)
    y = int(ratio.get("y") * scalar)

    # y height -40 for windows title
    window.resizeTo(x, y + 40)
    window.moveTo(20, 20)

    print(f'{ happy() }: Window minimized to { colored(x, "red") } x { colored(y, "red") } pixels')

    # wait for the window to be active
    await wait(delay.get("overwatch"))

    window.activate()


# async wait
async def wait(seconds):

    print(f'{ happy() }: waiting { colored(str(seconds) + "s", "red") }')
    await asyncio.sleep(seconds)

    window.activate()


# types the name and password in the sign in boxes
async def signin():

    window.activate()

    print(f'{ happy() }: Signing in..')

    # [name, password] to python object
    creds = os.getenv("PASSWORD").replace("[", "").replace("]", "").split(", ")

    # sign in
    py.write(creds[0], interval=_typing_delay)
    py.hotkey("tab")
    py.write(creds[1], interval=_typing_delay)
    py.hotkey("enter")

    await wait(delay.get("overwatch"))

# preps from import icon
async def prep():


    # Invalid Code
    pyperclip.copy(__default__code)

    # Overwatch does not update the clipboard without this
    # (ya need the delay too)
    window.minimize()

    # Animation Delay
    await asyncio.sleep(_animation_delay)

    # if not working its just this issue
    window.restore()

    # Animation Delay
    await asyncio.sleep(_animation_delay)

    # tap the "PASTE" icon
    # 🍺 (tab),  ⏩ (right) ⏩ (right) ⏩ (right) ⏩ (right) ⏩ (right), 🌌 (space)
    py.hotkey("tab")
    py.hotkey("right")
    py.hotkey("right")
    py.hotkey("right")
    py.hotkey("right")
    py.hotkey("right")
    py.hotkey("space")

    # Animation Delay
    await asyncio.sleep(_animation_delay)

    # Accept Warning
    # ⬇️ (down), 🌌 (space)
    py.hotkey("down")
    py.hotkey("space")

    # Animation Delay
    await asyncio.sleep(_animation_delay)

    # tap the "IMPORT" icon
    # ◀️ (left), ◀️ (left), ◀️ (left), ◀️ (left), 🌌 (space)
    py.hotkey("left")
    py.hotkey("left")
    py.hotkey("left")
    py.hotkey("left")
    py.hotkey("space")


# Navigates from the Welcome page to the Download page
async def fromWelcomeToDownload():

    window.activate()

    print(f'{ happy() }: navigating from { colored("Welcome", "green") } to { colored("Download", "blue") }')

    # Animation Delay
    await asyncio.sleep(_animation_delay)

    # tap "PLAY"
    # ⬇️ (down), 🌌 (space)
    py.hotkey("down")
    py.hotkey("space")

    # Animation Delay
    await asyncio.sleep(_animation_delay)

    # tap "GAME BROWSER"
    # Note: (left) x2, (space) will not work if there is an experimental card
    # ⏩ (right), ⏩ (right), ⏩ (right), ⏩ (right), 🌌 (space)
    py.hotkey("right")
    py.hotkey("right")
    py.hotkey("right")
    py.hotkey("right")
    py.hotkey("space")

    # Animation Delay
    await asyncio.sleep(_animation_delay)

    # tap "CREATE"
    # 🍺 (tab), 🍺 (tab), 🍺 (tab), 🍺 (tab), 🌌 (space)
    py.hotkey("tab")
    py.hotkey("tab")
    py.hotkey("tab")
    py.hotkey("tab")
    py.hotkey("space")

    # Minor Network Delay
    await asyncio.sleep(delay.get("ow_lobby"))

    # tap "SETTINGS"
    # ◀️ (left), ⏫ (up), ◀️ (left), 🌌 (space)
    py.hotkey("left")
    py.hotkey("up")
    py.hotkey("left")
    py.hotkey("space")

    global _dataManager
    _dataManager = bootArchive()

    await prep()


# import and copy a Workshop Game
async def download(code):

    window.activate()

    # does this code already exist ?
    if _dataManager.doesExist(code):
        print(f'{ sad() }: { colored(code, "magenta") } is already downloaded')
        return True

    print(f'{ happy() }: downloading { colored(code, "magenta") }', end=" ", flush=True)

    # Animation Delay
    await asyncio.sleep(_animation_delay)
    
    # Import Code
    # 🎹 (write), 💖 (enter)
    py.write(code, interval=_typing_delay)
    py.hotkey("enter")

    # Major Network Delay
    await asyncio.sleep(delay.get("download"))

    # tap the "COPY" icon
    # ⏩ (right), ⏩ (right), ⏩ (right), 🌌 (space)
    py.hotkey("right")
    py.hotkey("right")
    py.hotkey("right")
    py.hotkey("space")
    
    # Animation Delay
    await asyncio.sleep(_animation_delay)

    # if the import text is in the first 64
    # @x9v0
    failed = bool(
        0 < pyperclip.paste().find('Description: "Whoops.. Import Error D:"', 0, 64) or
        16 > len(pyperclip.paste())
    )

    if failed:

        print(colored("(failed)", "red", attrs=["blink", "bold"]))
        print(colored("    • INVALID CODE"))

    else:

        # Save file to archive
        def __archive(code, text):
            _dataManager.addToArchive(code, text)

        # Archive Data (temporary non daemon thread)
        Thread(target=__archive, args=(code, pyperclip.paste(),)).start()

        print("(done)")

    # next download
    py.hotkey("tab")
    await prep()

    return not failed