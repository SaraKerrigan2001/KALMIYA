import os

paths = {
    'notepad': r'C:\Windows\System32\notepad.exe',
    'discord': r'C:\Path\To\Discord.exe'
}

def open_notepad():
    os.startfile(paths['notepad'])

def open_discord():
    os.startfile(paths['discord'])