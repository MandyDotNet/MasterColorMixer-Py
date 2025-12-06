# monolithic style: UI and API 

# https://fastapi.tiangolo.com/reference/fastapi/
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from .core.mixing import ColorMixerService, MixResult
from .data.repo import ColorRecord
from .adapters.tts_pyttsx3 import speak_color_name

app = FastAPI(title="MasterColorMixer")
service = ColorMixerService()

#todo - add HTML for user interaction, scripting for the js logic and behavior
@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return """

    """

#--- API ---
# contracts for the API and FastAPI documentation, and FastAPI JSON conversion
class ColorDTO(BaseModel):
    name: str
    r: int
    y: int
    b: int
    is_base: bool

    @classmethod
    def from_record(cls, rec: ColorRecord) -> "ColorDTO":
        return cls(
            name = rec.name,
            r = rec.r,
            y = rec.y,
            b = rec.b,
            is_base = rec.is_base,
        )

class MixRequest(BaseModel):
    color_a: str
    color_b: str

class MixResponse(BaseModel):
    result: ColorDTO
    added_to_palette: bool
    palette_size: int

class SpeakRequest(BaseModel):
    name: str

class SpeakResponse(BaseModel):
    spoken: bool
    name: str

# --- Palette endpoints ---
@app.get("/api/palette", response_model=List[ColorDTO])
def get_palette() -> List[ColorDTO]:
    palette = service.get_palette()
    return [ColorDTO.from_record(c) for c in palette]

@app.post("/api/palette/clear", response_model=List[ColorDTO])
def clear_palette() -> List[ColorDTO]:
    palette = service.clear_palette()
    return [ColorDTO.from_record(c) for c in palette]


# --- Mix endpoint ---
@app.post("/api/mix", response_model=MixResponse)
def mix_colors_endpoint(payload: MixRequest) -> MixResponse:
    try:
        mix_result: MixResult = service.mix(payload.color_a, payload.color_b)
    except ValueError as e:
        raise HTTPException(status_code = 400, detail = str(e))

    return MixResponse(
        result = ColorDTO.from_record(mix_result.result),
        added_to_palette = mix_result.added_to_palette,
        palette_size = mix_result.palette_size,
    )


# --- Text-to-speech endpoint ---
@app.post("/api/speak", response_model=SpeakResponse)
def speak_endpoint(payload: SpeakRequest) -> SpeakResponse:
    # If speak_color_name raises, return 500 to the client.
    try:
        speak_color_name(payload.name)
    except Exception as e:  # you can narrow this later
        raise HTTPException(status_code = 500, detail = f"TTS error: {e}")

    return SpeakResponse(spoken = True, name = payload.name)