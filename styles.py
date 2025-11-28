from api_util import Check
from typing import TypedDict

class Background(TypedDict):
    color

class StylingLibrary():
    styles = {}

#source of truth
stylesLibrary = StylingLibrary()

def background(css:str, color = False, image = False, repeat = False, position = False, attachment = False, origin = False, clip = False):
    bools = {
        "-color":color,
        "-image":image,
        "-repeat":repeat,
        "-position":position,
        "-attachment":attachment,
        "-origin":origin,
        "-clip":clip
    }
    Check.none(css)
    for suffix, enabled in bools.items():
        if enabled:
            return f"background{suffix}:{css}"
    return f"background:{css}"

bg = globals()["background"]
if bg:
    color = "-color"
    image = "-image"
    repeat = "-repeat"
    position = "-position"
    attachent = "-attachment"
    origin = "-origin"
    clip = "clip"