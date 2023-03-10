import yaml 
from pathlib import Path
import dpath 
from pymediainfo import MediaInfo
from pprint import pprint
import sys 
from os import system, name
from time import monotonic

def clear():
 
    # for windows
    if name == 'nt':
        _ = system('cls')
 
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

p = Path(sys.argv[1])
SEARCH_LANGS = ["Bulgarian", "bg", "bul"]
SEARCH_TAGS = ["bg", "bul", "bulgarian"]
TAG_SEPARATOR = "."

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

d = {}
for item in p.rglob("*"):
    print(f"Checking {item}")
    if not item.is_dir():
        reason = ""
        
        if intersection(SEARCH_TAGS, item.name.split(TAG_SEPARATOR)):
         reason += "Name Tag | "
        
        try:
            info = MediaInfo.parse(item.as_posix())
        except Exception as ex:
            print(f"Failed to parse {item}: {ex}")
            continue
        
        for track in info.tracks:
            if track.language is None:
                continue
            if intersection(SEARCH_LANGS, track.other_language):
                reason += f"{track.track_type} {track.track_id} track | "
                
        if reason:
            print("Match!")
            d = dpath.new(d, item.as_posix(), reason.strip().strip("|").strip())
        clear()

with open(f"media_language_scan_{int(monotonic()*1000)}.yaml", "w") as f:
    yaml.dump(d, f)