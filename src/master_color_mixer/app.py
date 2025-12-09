# monolithic style: UI and API

import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .core.mixing import ColorMixerService, MixResult
from .data.repo import ColorRecord
from .adapters.tts_pyttsx3 import speak_color_name

logger = logging.getLogger(__name__)

#--- Lifespan: for startup/shutdown hooks ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up: creating ColorMixerService")
    app.state.color_service = ColorMixerService()

    try:
        yield
    finally:
        # ColorMixerService needs explicit cleanup
        logger.info("Application shutting down: clean up services")
        # app.state.color_service.close()
        logger.info("Shutdown complete")
#--- end Lifespan ---

app = FastAPI(title = "MasterColorMixer", lifespan = lifespan)
# service = ColorMixerService()

BASE_DIR = Path(__file__).resolve().parent
templates_dir = BASE_DIR / "templates"
static_dir = BASE_DIR / "static"
images_dir = BASE_DIR / "images"

app.mount("/static", StaticFiles(directory=static_dir), name = "static")
app.mount("/images", StaticFiles(directory=images_dir), name = "images")

# dependency to get ColorMixerService from app.state
def get_color_service(request: Request) -> ColorMixerService:
    return request.app.state.color_service

# root page
@app.get("/", response_class = HTMLResponse)
def index() -> HTMLResponse:
    index_path = templates_dir / "index.html"
    return HTMLResponse(index_path.read_text(encoding = "utf-8"))

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
@app.get("/api/palette", response_model = List[ColorDTO])
def get_palette(
    service: ColorMixerService = Depends(get_color_service),
    ) -> List[ColorDTO]:
    palette = service.get_palette()
    return [ColorDTO.from_record(c) for c in palette]

@app.post("/api/palette/clear", response_model = List[ColorDTO])
def clear_palette(
    service: ColorMixerService = Depends(get_color_service),
    ) -> List[ColorDTO]:
    palette = service.clear_palette()
    return [ColorDTO.from_record(c) for c in palette]


# --- Mix endpoint ---
@app.post("/api/mix", response_model = MixResponse)
def mix_colors_endpoint(
    payload: MixRequest,
    service: ColorMixerService = Depends(get_color_service),
    ) -> MixResponse:
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
@app.post("/api/speak", response_model = SpeakResponse)
def speak_endpoint(payload: SpeakRequest) -> SpeakResponse:
    # if speak_color_name raises, return 500 to the client.
    try:
        speak_color_name(payload.name)
    except Exception as e: 
        raise HTTPException(status_code = 500, detail = f"TTS error: {e}")

    return SpeakResponse(spoken = True, name = payload.name)