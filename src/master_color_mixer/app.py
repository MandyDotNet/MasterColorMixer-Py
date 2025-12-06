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
    <html lang = "en">
    <head>
        <meta charset = "utf-8">
        <title>MasterColorMixer</title>
        <style>
        :root {
            --circle-size: 120px; /* will be adjusted in JS based on palette size */
        }

        * {
            box-sizing: border-box;
        }

        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
            padding: 1.5rem;
            margin: 0;
            background: #f5f5f5;
            color: #222;
        }

        h1 {
            margin: 0 0 0.5rem 0;
            font-size: 2rem;
        }

        h2 {
            margin: 0 0 0.5rem 0;
            font-size: 1.4rem;
        }

        p {
            margin: 0.25rem 0 0.75rem 0;
        }

        main {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        /* Palette section */
        #palette-section {
            background: #ffffff;
            border-radius: 16px;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
            min-height: 180px;
        }

        #palette-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 0.75rem;
            flex-wrap: wrap;
        }

        #palette-title-row {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        #palette-help {
            font-size: 0.95rem;
            color: #555;
        }

        #palette-container-wrapper {
            display: flex;
            flex-direction: row;
            align-items: center;
            gap: 0.75rem;
        }

        #clearPaletteBtn {
            padding: 0.6rem 1rem;
            border-radius: 999px;
            border: none;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            background: #f44336;
            color: #ffffff;
            min-width: 120px;
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
            min-height: 140px;
            max-height: 220px;  /* fixed height: palette area does not grow */
            align-items: center;
        }

        .color-btn {
            width: var(--circle-size);
            height: var(--circle-size);
            border-radius: 999px;
            border: 3px solid #333;
            font-size: 0.9rem;
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

        /* Mixing section */
        #mix-section {
            background: #ffffff;
            border-radius: 16px;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
            min-height: 220px;  /* keep mixing area size stable */
        }

        #mix-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.75rem;
            flex-wrap: wrap;
            margin-bottom: 0.75rem;
        }

        #mix-buttons {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }

        .action-btn {
            padding: 0.7rem 1.4rem;
            border-radius: 999px;
            border: none;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            touch-action: manipulation;
        }

        #mixBtn {
            background: #4CAF50;
            color: #ffffff;
        }

        #clearBowlBtn {
            background: #FFC107;
            color: #222;
        }

        .action-btn:focus-visible {
            outline: 3px solid #000;
            outline-offset: 2px;
        }

        #mix-instructions {
            font-size: 0.95rem;
            color: #555;
            margin-top: 0.25rem;
        }

        .mix-bowl {
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            gap: 1.5rem;
            margin-top: 0.75rem;
            min-height: 160px;
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

        .drop-hint {
            font-size: 0.85rem;
            color: #666;
            text-align: center;
            margin-top: 0.25rem;
        }

        #remove-zone {
            margin-top: 0.5rem;
            text-align: center;
            font-size: 0.85rem;
            color: #555;
        }

        #status {
            margin-top: 1rem;
            font-size: 1.05rem;
            min-height: 1.4em;
        }

        #status strong {
            font-weight: 700;
        }

        @media (max-width: 640px) {
            body {
            padding: 1rem;
            }
            .mix-bowl {
            flex-direction: row;
            gap: 1rem;
            }
            .mix-slot {
            width: 120px;
            height: 120px;
            }
        }
        </style>
    </head>
    <body>
        <header>
        <h1>MasterColorMixer</h1>
        <p>Tap or drag colors into the bowl. Mix two colors to discover new ones.</p>
        </header>

        <main>
        <!-- Palette at the top -->
        <section id = "palette-section" aria-label = "Color palette">
            <div id = "palette-header">
            <div id = "palette-title-row">
                <h2>Palette</h2>
            </div>
            <div id = "palette-help">
                Tap a color to hear its name and add it to the bowl.<br />
                Drag a color into a bowl circle too.
            </div>
            </div>

            <div id = "palette-container-wrapper">
            <button
                id = "clearPaletteBtn"
                type = "button"
                aria-label = "Reset palette to starting colors"
            >
                Reset Palette
            </button>
            <div
                id = "palette"
                role = "list"
                aria-label = "Available colors"
            ></div>
            </div>
        </section>

        <!-- Mixing bowl -->
        <section id = "mix-section" aria-label = "Mixing bowl">
            <div id = "mix-header">
            <div>
                <h2>Mixing Bowl</h2>
                <p id = "mix-instructions">
                Put up to <strong>two</strong> colors in the bowl. No more than two at a time.
                </p>
            </div>
            <div id = "mix-buttons">
                <button id = "mixBtn" class = "action-btn" type = "button">
                Mix Colors
                </button>
                <button id = "clearBowlBtn" class = "action-btn" type = "button">
                Clear Bowl
                </button>
            </div>
            </div>

            <div class = "mix-bowl" aria-label = "Mixing slots">
            <div
                id = "slotA"
                class = "mix-slot"
                data-slot = "A"
                aria-label = "First color slot"
            >
                Slot A
            </div>
            <div
                id = "slotB"
                class = "mix-slot"
                data-slot = "B"
                aria-label = "Second color slot"
            >
                Slot B
            </div>
            </div>
            <div class = "drop-hint">
            Tip: Drag a filled color circle out of the bowl and drop it on the palette to remove it.
            </div>
            <div id = "remove-zone" aria-hidden = "true">
            The bowl never changes size. Only two colors fit at a time.
            </div>

            <div id = "status" aria-live = "polite"></div>
        </section>
        </main>

    <script>
    let slotA = null;
    let slotB = null;

    /**
        * Adjust circle size based on how many colors are in the palette.
        * Toddlers shouldn't have to scroll, so we shrink circles gently
        * as the palette grows.
        */
    function adjustCircleSize(count) {
        let size;
        if (count < =  6) {
        size = 120;
        } else if (count < =  10) {
        size = 105;
        } else if (count < =  14) {
        size = 90;
        } else if (count < =  18) {
        size = 80;
        } else if (count < =  24) {
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

    /**
        * Fetch palette from backend and render buttons.
        * /api/palette returns a JSON array of color objects:
        * [{ name, r, y, b, is_base }, ...]
        */
    async function fetchPalette() {
        try {
        const res = await fetch("/api/palette");
        if (!res.ok) {
            setStatus("Could not load palette.");
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
            btn.setAttribute("type", "button");
            btn.setAttribute("role", "listitem");
            btn.setAttribute("aria-label", c.name + " color");
            // We are using r, y, b as approximate RGB for display
            btn.style.backgroundColor = `rgb(${c.r}, ${c.y}, ${c.b})`;
            btn.textContent = c.name;

            // Click: add to bowl + speak name
            btn.onclick = ()  = > {
            addToBowl(c.name);
            speakColor(c.name);
            };

            // Drag: allow drag into bowl
            btn.draggable = true;
            btn.addEventListener("dragstart", (e)  = > {
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
        setStatus("Network error while loading palette.");
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

        // Make the filled slot draggable so toddler can drag it out
        el.draggable = true;
        el.addEventListener("dragstart", handleSlotDragStart);
        } else {
        el.textContent = emptyLabel;
        el.setAttribute("aria-label", emptyLabel);
        el.draggable = false;
        el.removeEventListener("dragstart", handleSlotDragStart);
        }
    }

    /**
        * Add a color to the bowl, obeying "max two colors" rule.
        */
    function addToBowl(name) {
        if (!slotA) {
        slotA = name;
        } else if (!slotB) {
        slotB = name;
        } else {
        setStatus("The bowl already has two colors. Clear or remove one first.");
        return;
        }
        renderSlots();
        setStatus("Added " + name + " to the bowl.");
    }

    /**
        * Clear bowl.
        */
    function clearBowl() {
        slotA = null;
        slotB = null;
        renderSlots();
        setStatus("Bowl cleared.");
    }

    /**
        * Drag from a slot: we encode which slot and which color.
        */
    function handleSlotDragStart(e) {
        const el = e.currentTarget;
        const slotId = el.id = = = "slotA" ? "A" : "B";
        const name = slotId = = = "A" ? slotA : slotB;
        e.dataTransfer.setData("text/plain", JSON.stringify({
        type: "slot",
        slot: slotId,
        name
        }));
        e.dataTransfer.effectAllowed = "move";
    }

    /**
        * Drop handler for bowl slots.
        */
    function setupBowlDropZones() {
        const slotADiv = document.getElementById("slotA");
        const slotBDiv = document.getElementById("slotB");

        [slotADiv, slotBDiv].forEach((el)  = > {
        el.addEventListener("dragover", (e)  = > {
            e.preventDefault();
            e.dataTransfer.dropEffect = "move";
        });

        el.addEventListener("drop", (e)  = > {
            e.preventDefault();
            const dataStr = e.dataTransfer.getData("text/plain");
            if (!dataStr) return;
            let payload;
            try {
            payload = JSON.parse(dataStr);
            } catch {
            return;
            }

            const targetSlot = el.id = = = "slotA" ? "A" : "B";

            // Only allow two colors total
            if (slotA && slotB && payload.type = = = "palette") {
            setStatus("The bowl already has two colors. Clear or remove one first.");
            return;
            }

            if (payload.type = = = "palette") {
            // Dropping a palette color into a slot
            if (targetSlot = = = "A") {
                slotA = payload.name;
            } else {
                slotB = payload.name;
            }
            renderSlots();
            speakColor(payload.name);
            setStatus("Added " + payload.name + " to " + el.id + ".");
            } else if (payload.type = = = "slot") {
            // Moving or swapping between slots
            const fromSlot = payload.slot;
            const fromName = payload.name;

            if (fromSlot = = = targetSlot) {
                // Dropped back onto same slot: no change
                return;
            }

            if (fromSlot = = = "A" && targetSlot = = = "B") {
                slotB = fromName;
                slotA = null;
            } else if (fromSlot = = = "B" && targetSlot = = = "A") {
                slotA = fromName;
                slotB = null;
            }
            renderSlots();
            setStatus("Moved " + fromName + " in the bowl.");
            }
        });
        });
    }

    /**
        * Make palette a drop zone to remove colors from bowl.
        * Dragging a filled slot onto the palette clears that slot.
        */
    function setupPaletteDropZone() {
        const palette = document.getElementById("palette");

        palette.addEventListener("dragover", (e)  = > {
        e.preventDefault();
        e.dataTransfer.dropEffect = "move";
        });

        palette.addEventListener("drop", (e)  = > {
        e.preventDefault();
        const dataStr = e.dataTransfer.getData("text/plain");
        if (!dataStr) return;
        let payload;
        try {
            payload = JSON.parse(dataStr);
        } catch {
            return;
        }

        if (payload.type = = = "slot") {
            if (payload.slot = = = "A") {
            slotA = null;
            } else if (payload.slot = = = "B") {
            slotB = null;
            }
            renderSlots();
            setStatus("Removed " + payload.name + " from the bowl.");
        }
        });
    }

    /**
        * Call backend TTS to speak a color name.
        */
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

    /**
        * Mix colors currently in the bowl.
        * POST /api/mix { color_a, color_b }
        */
    async function mix() {
        if (!slotA || !slotB) {
        setStatus("Pick two colors in the bowl first.");
        return;
        }
        try {
        const res = await fetch("/api/mix", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ color_a: slotA, color_b: slotB })
        });
        if (!res.ok) {
            const err = await res.json().catch(()  = > ({}));
            setStatus(err.detail || "Mix failed.");
            return;
        }
        const data = await res.json();
        const resultName = data.result.name;

        setStatus("Result: " + resultName + " (added to palette: " + (data.added_to_palette ? "yes" : "no") + ")");
        await fetchPalette();
        await speakColor(resultName); // speak mixed color name
        } catch (e) {
        console.error(e);
        setStatus("Network error while mixing.");
        }
    }

    /**
        * Reset palette via backend, keep bowl as-is or clear (your choice).
        */
    async function clearPalette() {
        try {
        await fetch("/api/palette/clear", { method: "POST" });
        await fetchPalette();
        setStatus("Palette reset to starting colors.");
        } catch (e) {
        console.error(e);
        setStatus("Could not reset palette.");
        }
    }

    document.addEventListener("DOMContentLoaded", ()  = > {
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