
"""
     .::::::.::::::::::::   ...    :::::::..   .        : .-:.     ::-.
    ;;;`    `;;;;;;;;''''.;;;;;;;. ;;;;``;;;;  ;;,.    ;;; ';;.   ;;;;'
    '[==/[[[[,    [[    ,[[     "[[,[[[,/[[['  [[[[, ,[[[[,  '[[,[[['  
      '''    $    $$    $$$,     $$$$$$$$$c    $$$$$$$$"$$$    c$$"    
     88b    dP    88,   "888,_ _,88P888b "88bo,888 Y88" 888o ,8P"`     
      "YMmMY"     MMM     "YMMMMMP" MMMM   "W" MMM  M'  "MMMmM"  

                    # ❤️🧡 OW PET v0.0 💚💜  #
                     # 💛 Author: Stormy 💙 #

    * Automation for (aka) Overwatch Workshop code delivery (OWCD)
    * Peripheral for https://workshopcodes.com/ (import feature)

    > (discord): https://discord.workshopcodes.com/
    > (twitter): https://twitter.com/OWModding
"""

# Native Packages
import asyncio, sys

# Additional Packages
from options import newConfig
from termcolor import colored

# package
from automate import quitOverwatch, overwatch, wait, signin, fromWelcomeToDownload, download
from timings import delay
from queueHandler import bootQueue
from emoji import sad
from errors import InvalidVariables

# queue data
# queue = ['vcc9v', 'W468T']
isQuit = False


# Main Process
async def process(q):

    # Queue thread will dump items
    # Are any items in the dump?
    newCode = q.getNext()


    # if there is a new item, download it
    if newCode:

        # Automate workshop download process
        await download(newCode)

        # Delete item from queue
        # It makes a new thread that will stop quits
        q.deleteCode(newCode)


    # Add a delay for data files
    # Online queues will not need this
    else:
        await asyncio.sleep(delay.get("interval"))


# start PET
async def start():

    # inject variables
    await newConfig()

    # quit overwatch if it's running
    # only works on windows (so does overwatch though)
    await quitOverwatch()

    # start overwatch and wait for the sign in boxes
    await overwatch()

    # sign in with values and wait for the welcome page
    await signin()

    # navigate from the welcome page to the download box
    await fromWelcomeToDownload()

    # start the queue process on a seperate thread
    # it's best to start this later because of the 20 window
    q = bootQueue()

    # manage queue and push codes
    while not isQuit:

        await process(q)


# Error Handler
try:

    asyncio.run(start())

except KeyboardInterrupt:

    print(colored("\nQuitting Python", "magenta", attrs=["bold"]))
    print(sad() + ":", "adios amigo")
    # sys.exit(0)

except InvalidVariables:

    sys.exit(2)

except Exception:

    raise
    


