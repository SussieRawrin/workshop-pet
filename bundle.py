
import os

# generate executable
# https://pyinstaller.readthedocs.io/en/stable/man/pyi-makespec.html

name = "Workshop Archive"

parameters = [

    # "--exclude-module boto3"
    # "--onefile",
    # "--key hoop",

    "--console",
    "--specpath spec",
    "--name bundle",

    f'--name "{ name }"',

    # "--add-data icons/overwatch.ico;spec/icons/overwatch.ico"

    # # Mac and Windows specific
    "--icon icons/overwatch.ico",
]

install = [

    "--noconfirm",
    # "--clean",

    "--distpath ../dist",
]

try:
    os.system(f'cd python && pyi-makespec { " ".join(parameters) } __init__.py && pyinstaller { " ".join(install) } "spec/{ name }.spec" && cd ..')
    print("done")

except:
    print("failed")
    raise
