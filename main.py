import yaml 
from pathlib import Path
import dpath 
from pymediainfo import MediaInfo
from pprint import pprint

p = Path("/home/vasko/Downloads")
SEARCH_LANGS = ["Bulgarian", "bg", "bul"]
SEARCH_TAGS = ["Bulgarian", "bg", "bul"]
TAG_SEPARATOR = "."

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

d = {}
for item in p.rglob("*"):
    if not item.is_dir():
        reason = ""
        
        if intersection(SEARCH_TAGS, item.name.split(TAG_SEPARATOR)):
         reason += "Name Tag "
         
        info = MediaInfo.parse(item.as_posix())
        for track in info.tracks:
            if track.language is None:
                continue
            if intersection(SEARCH_LANGS, track.other_language):
                reason += f"{track.track_type} {track.track_id} track "
                
        if reason:
            d = dpath.new(d, item.as_posix(), reason.strip())
        
with open("media_language_scan.yaml", "w") as f:
    yaml.dump(d, f)