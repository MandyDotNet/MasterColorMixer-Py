console.log("MasterColorMixer JS loaded");

let slotA = null;
let slotB = null;

// This RYB system I wanted to use turned into a can of worms.
// Luckily, someone else figured out the technique, so I have implemented their idea in rybToRgb()
// https://math.stackexchange.com/questions/305395/ryb-and-rgb-color-space-conversion

// convert a RYB triple (0-255 each) into an RGB triple (0-255 each).
function rybToRgb(r, y, b) {
    let R = r;
    let Y = y;
    let B = b;

    // remove shared "whiteness"
    const white = Math.min(R, Y, B);
    R -= white;
    Y -= white;
    B -= white;

    const maxYellow = Math.max(R, Y, B);

    // extract green from yellow and blue
    let G = Math.min(Y, B);
    Y -= G;
    B -= G;

    // boost mixed blue/green to keep them vivid
    if (B > 0 && G > 0) {
        B *= 2;
        G *= 2;
    }

    // spread any remaining yellow into red + green
    R += Y;
    G += Y;

    // normalize so brightness stays similar to original yellow
    const maxGreen = Math.max(R, G, B);
    if (maxGreen > 0) {
        const n = maxYellow / maxGreen;
        R *= n;
        G *= n;
        B *= n;
    }

    // add the white back in
    R += white;
    G += white;
    B += white;

    // clamp + round to 0–255 ints
    const clamp = (v) => Math.max(0, Math.min(255, Math.round(v)));
    return [clamp(R), clamp(G), clamp(B)];
}

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

            const [R, G, B] = rybToRgb(c.r, c.y, c.b);
            btn.style.backgroundColor = `rgb(${R}, ${G}, ${B})`;

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

            if (slotA && slotB && payload.type === "palette") {
                setStatus("Two colors only. Clear or remove one.");
                return;
            }

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
            headers: { "Content-Type": "application/json" },
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
            headers: { "Content-Type": "application/json" },
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