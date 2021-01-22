
# Native Packages
import os, subprocess, sys, asyncio, time
from threading import Thread

# Additional Dependencies
from termcolor import colored, cprint
import pyperclip

# Automation Packages
import pyautogui as py

# use px when py does not work (video games)
# import pydirectinput as px
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


# finds an image on display
def findImage(image, _confidence=.9, _grayscale=False):

    # confidence needs
    # pip install opencv-python
    _size = 'md'

    # window.activate()
    return py.locateCenterOnScreen(f'python{ os.path.sep }animations{ os.path.sep }{ _size }{ os.path.sep }{ image }.png', confidence=_confidence, grayscale=_grayscale)

# waits for an image on display
async def waitForImage(image, _confidence=.9, _grayscale=False, timeout=0):

    if timeout > 0:
        start = time.time()

    position = findImage(image, _confidence=_confidence, _grayscale=_grayscale)

    while (not position):

        if timeout > 0 and time.time() > start + timeout:
            return position

        await asyncio.sleep(delay["image_polling"])
        position = findImage(image, _confidence=_confidence, _grayscale=_grayscale)

    # testing
    # await asyncio.sleep(delay["image_polling"])
    return position

# waits for an image on display to disappear
async def waitForNotImage(image, _confidence=.9, _grayscale=False, timeout=0):

    if timeout > 0:
        start = time.time();

    position = findImage(image, _confidence=_confidence, _grayscale=_grayscale)

    while (position):

        if timeout > 0 and time.time() > start + timeout:
            return False

        await asyncio.sleep(delay["image_polling"])
        position = findImage(image, _confidence=_confidence, _grayscale=_grayscale)

    # testing
    # await asyncio.sleep(delay["image_polling"])
    return True

# video game
def click():
    py.mouseDown()
    py.mouseUp()

# kinda only needs to be done once to focus scree
# probably better to do it always
def clickAt(position):
    py.mouseDown(position)
    py.mouseUp(position)

# navigates by waiting for images and tapping them
async def navigate(*images):
    for image in images:
      clickAt(await waitForImage(image))




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

    print(f'{ happy() }: Waiting for { colored("Overwatch", "yellow", attrs=["bold"]) } window')

    # new window
    global window

    while not bool(window):
    
        if "Overwatch" not in pw.getAllTitles():
            await asyncio.sleep(delay["interval"])
            continue

        else:
            window = pw.getWindowsWithTitle("Overwatch")[0]

    # dimensions: [[ratio x, ratio y], scale]
    # dimensions = [[16, 9], 40]
    dimensions = [[1024, 576], 1]

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
    # py.moveTo(await waitForImage('login-dark'), duration=.09, tween=py.easeInOutCirc)
    # click to focus text (normal click will not work anymore for first focus)
    clickAt(await waitForImage('login-dark'))


# async wait
async def wait(seconds):

    print(f'{ happy() }: waiting { colored(str(seconds) + "s", "red") }')
    await asyncio.sleep(seconds)


# types the name and password in the sign in boxes
async def signin():

    print(f'{ happy() }: Signing in..')

    # [name, password] to python object
    creds = os.getenv("PASSWORD").replace("[", "").replace("]", "").split(", ")

    # sign in
    window.activate()
    py.write(creds[0], interval=_typing_delay)
    py.hotkey("tab")
    py.write(creds[1], interval=_typing_delay)
    
    # py.hotkey("enter")
    window.activate()
    clickAt(await waitForImage('login'))

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

    # paste workshop and navigate to download
    await navigate('paste', 'confirm', 'download')


# Navigates from the Welcome page to the Download page
async def fromWelcomeToDownload():

    window.activate()

    print(f'{ happy() }: navigating from { colored("Main Menu", "green") } to { colored("Download", "blue") }')

    # Animation Delay
    await waitForImage('add_friend')

    # exit custom game if joined back in
    if not await waitForImage('play', _grayscale=True, _confidence=.6, timeout=4):
        print(f'{ sad() }: exiting { colored("custom game", "blue") }')
        # navigating out of a joined custom game will go back to main menu
        await navigate('exit', 'yes')
    else:
        print('not in custom gaem')

    # tap "PLAY"
    clickAt(await waitForImage('play', _grayscale=True, _confidence=.6))
        
    # navigate from the "PLAY" page to the "CUSTOM GAME" settings page
    await navigate('game_browser', 'create', 'settings')

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

    # Animation Delay
    await asyncio.sleep(_animation_delay)

    # Wait for downloaded code
    downloaded = await waitForNotImage('default_workshop', timeout=delay.get("max_download"))

    if not downloaded:

        print(colored("(failed)", "red", attrs=["blink", "bold"]))
        print(colored("    • INVALID CODE"))

    else:

        # tap the "COPY" icon
        await navigate('copy')

        # if the import text is in the first 64
        # @x9v0
        failed = bool(
            0 < pyperclip.paste().find('Description: "Whoops.. Import Error D:"', 0, 64) or
            16 > len(pyperclip.paste())
        )

        if failed:

            print(colored("(failed)", "orange", attrs=["blink", "bold"]))
            print(colored("    • BAD COPY"))

        else:

            # Save file to archive
            def __archive(code, text):
                _dataManager.addToArchive(code, text)

            # Archive Data (temporary non daemon thread)
            Thread(target=__archive, args=(code, pyperclip.paste(),)).start()

            print("(done)")

    # Animation Delay
    await asyncio.sleep(_animation_delay)

    await prep()

    return downloaded