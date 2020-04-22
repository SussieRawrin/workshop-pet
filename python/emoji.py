
# native imports
import random

# Cool Emojis
happy_emojis = ("😁", "😋", "😊", "🌝", "🤤", "😜", "😝", "😌", "😂", "😅", "😇", "🍁", "🍄", "🐋", "🐳", "🐺", "🦇", "🌈", "🏳️‍🌈", "☄️", "🌊", "🌌", "👻", "🎂", "🍭", "🍩", "🍺", "🍻", "🥝", "🍌", "🍉", "🍧", "🍦", "🥧", "🍪", "🥙", "🥞", "🍳", "🍔", "🥩", "🥓", "🥚", "🍫", "🍬")

# Bad Emojis
sad_emojis = ("🙄", "😐", "😑", "😴", "😥", "😣", "😒", "😓", "😖", "😞", "😟", "😤", "😢", "😭", "😨", "😰", "😳", "😡", "😠", "🤬", "😷", "🤒", "🤕", "🤮", "🤧", "👿", "💀", "💩", "🌑", "🌧", "🏴‍☠️")

# Grab a Cool Emoji
def happy():
    return random.choice(happy_emojis)

# Grab a Bad Emoji
def sad():
    return random.choice(sad_emojis)