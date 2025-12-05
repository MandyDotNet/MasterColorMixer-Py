# monolithic style: UI and API 

# https://fastapi.tiangolo.com/reference/fastapi/
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from .core.mixing import ColorMixerService
from .data.repo import ColorDef
from .adapters.tts_pyttsx3 import speak_color_name

app = FastAPI(title="MasterColorMixer")
service = ColorMixerService()

#todo - add HTML for user interaction, scripting for the js logic and behavior
@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return """

    """

#--- API ---
# create color record dict
# create get palette function
# create clear palette function
# create mix function
# create speak function