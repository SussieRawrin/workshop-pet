
# Native Packages
import os, sys

# package
from emoji import sad, happy
from errors import InvalidVariables

# Additional Dependencies
# https://pypi.org/project/colored/

from dotenv import load_dotenv, dotenv_values
from termcolor import colored, cprint

# New Console
# @atexit.register
def clear():
    os.system('cls' if os.name=='nt' else 'clear')

clear()

# Allow colors on windows
os.system('color')

# which values are required?
variables = ("PASSWORD", "OVERWATCH_PATH")

# note optional variables are minicase
optional = (
    "window",
    
    "sqs_access_key_id",
    "sqs_secret_access_key",
    "queue_url",

    "s3_access_key_id",
    "s3_secret_access_key",
    "bucket_name",
    "optional_head_cache_prefix_uri",
    
    "region",
)

# processed values
values = dotenv_values()

# validate config
async def newConfig():

    # stash issues
    issues = []

    # injects values into os.getenv()
    load_dotenv()

    #? does the .env have each value
    #? is each value injected into os.getenv()
    for variable in variables:
        if not (variable in values.keys() and bool(os.getenv(variable))):
            issue = f'{ colored(variable, "magenta") } is not defined in { colored(".env", "magenta") }'
            issues.append(issue)
    
    #? are any values in .env not needed?
    for value in values.keys():
        if value not in variables and value not in optional:
            issue = f'{ colored(value, "magenta")} is not a permitted value in {colored(".env", "magenta") }'
            issues.append(issue)

    # print any issues and exit
    if issues:
        print()
        print(f'    { sad()} {colored("Application Issue ", "yellow", attrs=["bold"]) }')
        print("\t• ", end="")
        print("\n\t• ".join(issues))

        raise InvalidVariables
    
    # if there are no issues, keep going
    else:
        print(colored("PET", "green", attrs=['bold']) + colored(" initilizing...", "green", attrs=['blink']))
        print(happy() + ": " + colored("Application Values", "yellow", attrs=["bold"]))
        print(happy() + ": " + colored("Emoji", "magenta", attrs=["bold"]))
        print()





