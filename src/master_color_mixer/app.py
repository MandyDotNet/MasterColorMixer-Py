# monolithic style: UI and API 

# https://fastapi.tiangolo.com/reference/fastapi/
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from .core.mixing import ColorMixerService, MixResult
from .data.repo import ColorRecord
from .adapters.tts_pyttsx3 import speak_color_name

app = FastAPI(title = "MasterColorMixer")
service = ColorMixerService()

#todo - add HTML for user interaction, scripting for the js logic and behavior
@app.get("/", response_class = HTMLResponse)
def index() -> str:
    return """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>MasterColorMixer</title>
        <style>
        :root {
            --circle-size: 120px;
        }

        * {
            box-sizing: border-box;
        }

        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
            padding: 1.5rem;
            margin: 0;
            background:
            repeating-linear-gradient(
                45deg,
                #ffe5ec,
                #ffe5ec 20px,
                #fff9d9 20px,
                #fff9d9 40px
            );
            color: #222;
        }

        h1 {
            margin: 0 0 1rem 0;
            font-size: 2.2rem;
            text-align: center;
        }

        h2 {
            margin: 0 0 0.75rem 0;
            font-size: 1.5rem;
        }

        main {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
            max-width: 960px;
            margin: 0 auto;
        }

        /* Card containers */
        #palette-section,
        #mix-section {
            background: #ffffff;
            border-radius: 20px;
            padding: 1rem 1.25rem 1.25rem 1.25rem;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
        }

        /* Palette */
        #palette-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            flex-wrap: wrap;
            margin-bottom: 0.75rem;
        }

        #palette-container-wrapper {
            display: flex;
            flex-direction: row;
            align-items: center;
            gap: 0.75rem;
        }

        #clearPaletteBtn {
            padding: 0.7rem 1.2rem;
            border-radius: 999px;
            border: none;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            background: #f44336;
            color: #ffffff;
            min-width: 130px;
        }

        #clearPaletteBtn:focus-visible {
            outline: 3px solid #000;
            outline-offset: 2px;
        }

        #palette {
            flex: 1;
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
            padding: 0.25rem;
            min-height: 150px;
            max-height: 150px;
            align-items: center;
        }

        .color-btn {
            width: var(--circle-size);
            height: var(--circle-size);
            border-radius: 999px;
            border: 3px solid #333;
            font-size: 0.95rem;
            font-weight: 700;
            color: #111;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            outline: none;
            padding: 0.25rem;
            text-align: center;
            background: #ddd;
            touch-action: manipulation;
        }

        .color-btn:focus-visible {
            outline: 4px solid #000;
            outline-offset: 2px;
        }

        .color-btn.base-color {
            box-shadow: 0 0 0 3px #00000088;
        }

        /* Mixing bowl */
        #mix-header {
            display: flex;
            justify-content: center;
            margin-bottom: 0.5rem;
        }

        #mix-buttons {
            display: flex;
            justify-content: center;
            gap: 0.75rem;
            margin-bottom: 0.75rem;
            flex-wrap: wrap;
        }

        .action-btn {
            padding: 0.75rem 1.6rem;
            border-radius: 999px;
            border: none;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            touch-action: manipulation;
        }

        #mixBtn {
            background: #4caf50;
            color: #ffffff;
        }

        #clearBowlBtn {
            background: #ffc107;
            color: #222;
        }

        .action-btn:focus-visible {
            outline: 3px solid #000;
            outline-offset: 2px;
        }

        .mix-bowl-wrapper {
            background: #ffe9c7;
            border-radius: 24px;
            padding: 1rem;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 210px;
        }

        .mix-bowl {
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            gap: 2rem;
        }

        .mix-slot {
            width: 140px;
            height: 140px;
            border-radius: 999px;
            border: 3px dashed #777;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            background: #fafafa;
            text-align: center;
            padding: 0.5rem;
        }

        .mix-slot.filled {
            border-style: solid;
            color: #111;
        }

        .mix-slot.filled span {
            pointer-events: none;
        }

        #status {
            margin-top: 0.9rem;
            font-size: 1.05rem;
            min-height: 1.4em;
            text-align: center;
        }

        @media (max-width: 640px) {
            body {
            padding: 1rem;
            }
            .mix-bowl {
            gap: 1.2rem;
            }
            .mix-slot {
            width: 120px;
            height: 120px;
            }
        }
        </style>
    </head>
    <body>
        <h1>MasterColorMixer</h1>

        <main>
        <section id="palette-section" aria-label="Color palette">
            <div id="palette-header">
            <h2>Palette</h2>
            </div>
            <div id="palette-container-wrapper">
            <button
                id="clearPaletteBtn"
                type="button"
                aria-label="Reset palette to starting colors"
            >
                Reset Palette
            </button>
            <div
                id="palette"
                role="list"
                aria-label="Available colors"
            ></div>
            </div>
        </section>

        <section id="mix-section" aria-label="Mixing bowl">
            <div id="mix-header">
            <h2>Mixing Bowl</h2>
            </div>

            <div id="mix-buttons">
            <button id="mixBtn" class="action-btn" type="button">
                Mix Colors
            </button>
            <button id="clearBowlBtn" class="action-btn" type="button">
                Clear Bowl
            </button>
            </div>

            <div class="mix-bowl-wrapper">
            <div class="mix-bowl" aria-label="Mixing slots">
                <div
                id="slotA"
                class="mix-slot"
                data-slot="A"
                aria-label="First color slot"
                >
                Slot A
                </div>
                <div
                id="slotB"
                class="mix-slot"
                data-slot="B"
                aria-label="Second color slot"
                >
                Slot B
                </div>
            </div>
            </div>

            <div id="status" aria-live="polite"></div>
        </section>
        </main>

    <script>
    let slotA = null;
    let slotB = null;

    function adjustCircleSize(count) {
        let size;
        if (count <= 6) {
        size = 120;
        } else if (count <= 10) {
        size = 105;
        } else if (count <= 14) {
        size = 90;
        } else if (count <= 18) {
        size = 80;
        } else if (count <= 24) {
        size = 70;
        } else {
        size = 60;
        }
        document.documentElement.style.setProperty("--circle-size", size + "px");
    }

    function setStatus(msg) {
        const status = document.getElementById("status");
        status.textContent = msg || "";
    }

    async function fetchPalette() {
        try {
        const res = await fetch("/api/palette");
        if (!res.ok) {
            setStatus("Could not load colors.");
            return;
        }
        const data = await res.json();
        const container = document.getElementById("palette");
        container.innerHTML = "";

        adjustCircleSize(data.length);

        for (const c of data) {
            const btn = document.createElement("button");
            btn.className = "color-btn";
            if (c.is_base) {
            btn.classList.add("base-color");
            }
            btn.type = "button";
            btn.setAttribute("role", "listitem");
            btn.setAttribute("aria-label", c.name + " color");
            btn.style.backgroundColor = `rgb(${c.r}, ${c.y}, ${c.b})`;
            btn.textContent = c.name;

            btn.onclick = () => {
            addToBowl(c.name);
            speakColor(c.name);
            };

            btn.draggable = true;
            btn.addEventListener("dragstart", (e) => {
            e.dataTransfer.setData("text/plain", JSON.stringify({
                type: "palette",
                name: c.name
            }));
            e.dataTransfer.effectAllowed = "move";
            });

            container.appendChild(btn);
        }
        } catch (e) {
        console.error(e);
        setStatus("Network error while loading colors.");
        }
    }

    function renderSlots() {
        const slotADiv = document.getElementById("slotA");
        const slotBDiv = document.getElementById("slotB");

        renderSlot(slotADiv, slotA, "Slot A");
        renderSlot(slotBDiv, slotB, "Slot B");
    }

    function renderSlot(el, value, emptyLabel) {
        el.innerHTML = "";
        el.classList.remove("filled");
        el.style.backgroundColor = "#fafafa";

        if (value) {
        const span = document.createElement("span");
        span.textContent = value;
        el.appendChild(span);
        el.classList.add("filled");
        el.setAttribute("aria-label", emptyLabel + " with " + value);
        el.draggable = true;
        el.addEventListener("dragstart", handleSlotDragStart);
        } else {
        el.textContent = emptyLabel;
        el.setAttribute("aria-label", emptyLabel);
        el.draggable = false;
        el.removeEventListener("dragstart", handleSlotDragStart);
        }
    }

    function addToBowl(name) {
        if (!slotA) {
        slotA = name;
        } else if (!slotB) {
        slotB = name;
        } else {
        setStatus("Two colors only. Clear or remove one.");
        return;
        }
        renderSlots();
        setStatus("");
    }

    function clearBowl() {
        slotA = null;
        slotB = null;
        renderSlots();
        setStatus("");
    }

    function handleSlotDragStart(e) {
        const el = e.currentTarget;
        const slotId = el.id === "slotA" ? "A" : "B";
        const name = slotId === "A" ? slotA : slotB;
        e.dataTransfer.setData("text/plain", JSON.stringify({
        type: "slot",
        slot: slotId,
        name
        }));
        e.dataTransfer.effectAllowed = "move";
    }

    function setupBowlDropZones() {
        const slotADiv = document.getElementById("slotA");
        const slotBDiv = document.getElementById("slotB");

        [slotADiv, slotBDiv].forEach((el) => {
        el.addEventListener("dragover", (e) => {
            e.preventDefault();
            e.dataTransfer.dropEffect = "move";
        });

        el.addEventListener("drop", (e) => {
            e.preventDefault();
            const dataStr = e.dataTransfer.getData("text/plain");
            if (!dataStr) return;
            let payload;
            try {
            payload = JSON.parse(dataStr);
            } catch {
            return;
            }

            const targetSlot = el.id === "slotA" ? "A" : "B";

            if (payload.type === "palette") {
            if (targetSlot === "A") {
                slotA = payload.name;
            } else {
                slotB = payload.name;
            }
            renderSlots();
            speakColor(payload.name);
            setStatus("");
            } else if (payload.type === "slot") {
            const fromSlot = payload.slot;
            const fromName = payload.name;

            if (fromSlot === targetSlot) return;

            if (fromSlot === "A" && targetSlot === "B") {
                slotB = fromName;
                slotA = null;
            } else if (fromSlot === "B" && targetSlot === "A") {
                slotA = fromName;
                slotB = null;
            }
            renderSlots();
            setStatus("");
            }
        });
        });
    }

    function setupPaletteDropZone() {
        const palette = document.getElementById("palette");

        palette.addEventListener("dragover", (e) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = "move";
        });

        palette.addEventListener("drop", (e) => {
        e.preventDefault();
        const dataStr = e.dataTransfer.getData("text/plain");
        if (!dataStr) return;
        let payload;
        try {
            payload = JSON.parse(dataStr);
        } catch {
            return;
        }

        if (payload.type === "slot") {
            if (payload.slot === "A") {
            slotA = null;
            } else if (payload.slot === "B") {
            slotB = null;
            }
            renderSlots();
            setStatus("");
        }
        });
    }

    async function speakColor(name) {
        try {
        await fetch("/api/speak", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ name })
        });
        } catch (e) {
        console.error("TTS error", e);
        }
    }

    async function mix() {
        if (!slotA || !slotB) {
        setStatus("Pick two colors first.");
        return;
        }
        try {
        const res = await fetch("/api/mix", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ color_a: slotA, color_b: slotB })
        });
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            setStatus(err.detail || "Mix failed.");
            return;
        }
        const data = await res.json();
        const resultName = data.result.name;

        setStatus("");
        await fetchPalette();
        await speakColor(resultName);
        } catch (e) {
        console.error(e);
        setStatus("Network error while mixing.");
        }
    }

    async function clearPalette() {
        try {
        await fetch("/api/palette/clear", { method: "POST" });
        await fetchPalette();
        setStatus("");
        } catch (e) {
        console.error(e);
        setStatus("Could not reset palette.");
        }
    }

    document.addEventListener("DOMContentLoaded", () => {
        document.getElementById("mixBtn").onclick = mix;
        document.getElementById("clearBowlBtn").onclick = clearBowl;
        document.getElementById("clearPaletteBtn").onclick = clearPalette;

        setupBowlDropZones();
        setupPaletteDropZone();
        fetchPalette();
        renderSlots();
    });
    </script>
    </body>
    </html>

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
@app.get("/api/palette", response_model = List[ColorDTO])
def get_palette() -> List[ColorDTO]:
    palette = service.get_palette()
    return [ColorDTO.from_record(c) for c in palette]

@app.post("/api/palette/clear", response_model = List[ColorDTO])
def clear_palette() -> List[ColorDTO]:
    palette = service.clear_palette()
    return [ColorDTO.from_record(c) for c in palette]


# --- Mix endpoint ---
@app.post("/api/mix", response_model = MixResponse)
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
@app.post("/api/speak", response_model = SpeakResponse)
def speak_endpoint(payload: SpeakRequest) -> SpeakResponse:
    # If speak_color_name raises, return 500 to the client.
    try:
        speak_color_name(payload.name)
    except Exception as e:  # you can narrow this later
        raise HTTPException(status_code = 500, detail = f"TTS error: {e}")

    return SpeakResponse(spoken = True, name = payload.name)