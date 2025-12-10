console.log("MasterColorMixer JS loaded");

// current colors in the two mixing slots
let slotA = null;
let slotB = null;

// cache of the last palette data from the server
let lastPaletteData = null;
let lastPaletteSize = 0; // used so we only say "palette is full" once

function setStatus(msg) {
    const status = document.getElementById("status");
    status.textContent = msg || "";
}
/*
 * RYB to RGB conversion
 * adapted from:
 * https://math.stackexchange.com/questions/305395/ryb-and-rgb-color-space-conversion
 */
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

// decide if text on top of a color should be black or white
function idealTextColor(r, g, b) {
    const luminanceThreshold = 150;
    const luminance = (0.299 * r + 0.587 * g + 0.114 * b);
    return luminance > luminanceThreshold ? "#000000" : "#FFFFFF";
}

// layout the palette as a responsive grid of circles
function layoutPalette(container, count) {
    if (!container) return;

    const MAX_CAPACITY = 20;
    const MAX_COLUMNS = 10; // allow up to 10 columns
    const GAP = 8;          // gap between bubbles
    const MIN_SIZE = 32;    // minimum bubble diameter
    const MAX_SIZE = 120;   // maximum bubble diameter

    const effectiveCount = Math.min(count, MAX_CAPACITY);
    const columns = Math.max(1, Math.min(MAX_COLUMNS, effectiveCount));

    const containerWidth = Math.max(0, container.clientWidth);
    const totalGap = (columns - 1) * GAP;
    const rawSize = columns > 0 ? Math.floor((containerWidth - totalGap) / columns) : MIN_SIZE;
    const size = Math.max(MIN_SIZE, Math.min(MAX_SIZE, rawSize));

    container.style.display = "grid";
    container.style.gridTemplateColumns = `repeat(${columns}, ${size}px)`;
    container.style.gridAutoRows = `${size}px`;
    container.style.gap = `${GAP}px`;
    container.style.alignItems = "start";

    // make each child button a circle and scale font size
    Array.from(container.children).forEach((btn) => {
        btn.style.width = `${size}px`;
        btn.style.height = `${size}px`;
        btn.style.borderRadius = "50%";
        btn.style.display = "inline-flex";
        btn.style.alignItems = "center";
        btn.style.justifyContent = "center";
        //btn.style.overflow = "hidden";
        //btn.style.textOverflow = "ellipsis";
        //btn.style.whiteSpace = "nowrap";

        // slightly larger default font to stay readable
        const fontSize = Math.max(12, Math.floor(size / 4));
        btn.style.fontSize = `${fontSize}px`;

        const span = btn.querySelector("span");
        if (span) {
            span.style.pointerEvents = "none";
        }
    });
}

/*  Palette fetch & render  */

async function fetchPalette() {
    try {
        const res = await fetch("/api/palette");
        if (!res.ok) {
            setStatus("Could not load colors.");
            return;
        }

        const data = await res.json();

        const prevSize = lastPaletteData ? lastPaletteData.length : 0;
        lastPaletteData = data;
        lastPaletteSize = data.length;

        const container = document.getElementById("palette");
        if (!container) {
            console.error("Palette container not found");
            return;
        }

        container.innerHTML = "";

        const MAX_CAPACITY = 20;
        const showCount = Math.min(data.length, MAX_CAPACITY);

        // if the palette has just become full (or over capacity), speak a message once
        if (data.length >= MAX_CAPACITY && prevSize < MAX_CAPACITY) {
            speakColor("Your palette is full.");
        }

        // create a bubble button for each color (up to MAX_CAPACITY)
        for (const c of data.slice(0, MAX_CAPACITY)) {
            const btn = document.createElement("button");
            btn.className = "color-bubble";
            if (c.is_base) {
                btn.classList.add("base-color");
            }

            btn.type = "button";
            btn.setAttribute("role", "listitem");
            btn.setAttribute("aria-label", `${c.name} color`);

            const [R, G, B] = rybToRgb(c.r, c.y, c.b);
            btn.style.backgroundColor = `rgb(${R}, ${G}, ${B})`;
            btn.style.color = idealTextColor(R, G, B);

            const span = document.createElement("span");
            span.textContent = c.name;
            btn.appendChild(span);

            // clicking only speaks the color
            btn.addEventListener("click", () => {
                speakColor(c.name);
            });

            // dragging is how we add to the mixing bowl
            btn.draggable = true;
            btn.addEventListener("dragstart", (e) => {
                e.dataTransfer.setData(
                    "text/plain",
                    JSON.stringify({
                        type: "palette",
                        name: c.name,
                    })
                );
                e.dataTransfer.effectAllowed = "move";
            });

            container.appendChild(btn);
        }

        // layout the palette grid
        layoutPalette(container, showCount);
    } catch (e) {
        console.error(e);
        setStatus("Network error while loading colors.");
    }
}

/*  Mixing slots render */

function renderSlots() {
    const slotADiv = document.getElementById("slotA");
    const slotBDiv = document.getElementById("slotB");

    if (!slotADiv || !slotBDiv) {
        console.error("Mixing slots not found");
        return;
    }

    renderSlot(slotADiv, slotA, "Slot A");
    renderSlot(slotBDiv, slotB, "Slot B");
}

// look up color details from the cached palette by name
function findColorByName(name) {
    if (!lastPaletteData) return null;
    return lastPaletteData.find((c) => c.name === name) || null;
}

function renderSlot(el, value, emptyLabel) {
    el.innerHTML = "";
    el.classList.remove("filled");
    el.style.backgroundColor = "#fafafa";
    el.style.color = "#111";
    el.removeEventListener("dragstart", handleSlotDragStart);

    if (value) {
        const span = document.createElement("span");
        span.textContent = value;
        el.appendChild(span);
        el.classList.add("filled");
        el.setAttribute("aria-label", `${emptyLabel} with ${value}`);
        el.draggable = true;
        el.addEventListener("dragstart", handleSlotDragStart);

        // show the actual color in the slot background
        const colorObj = findColorByName(value);
        if (colorObj) {
            const [R, G, B] = rybToRgb(colorObj.r, colorObj.y, colorObj.b);
            el.style.backgroundColor = `rgb(${R}, ${G}, ${B})`;
            el.style.color = idealTextColor(R, G, B);
        }
    } else {
        el.textContent = emptyLabel;
        el.setAttribute("aria-label", emptyLabel);
        el.draggable = false;
    }
}

/*  Mixing bowl operations  */

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

    e.dataTransfer.setData(
        "text/plain",
        JSON.stringify({
            type: "slot",
            slot: slotId,
            name,
        })
    );
    e.dataTransfer.effectAllowed = "move";
}

/*  Drag & Drop   */

function setupBowlDropZones() {
    const slotADiv = document.getElementById("slotA");
    const slotBDiv = document.getElementById("slotB");

    if (!slotADiv || !slotBDiv) return;

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

            // if both slots are full and user drags in from palette, block it
            if (slotA && slotB && payload.type === "palette") {
                setStatus("Two colors only. Clear or remove one.");
                speakColor("Mixing bowl full");
                return;
            }

            if (payload.type === "palette") {
                // drag from palette into a slot fills that slot only
                if (targetSlot === "A") {
                    slotA = payload.name;
                } else {
                    slotB = payload.name;
                }
                renderSlots();
                speakColor(payload.name);
                setStatus("");
            } else if (payload.type === "slot") {
                // dragging between slots moves the color
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
    if (!palette) return;

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

        // dragging a color back onto the palette removes it from the bowl
        if (payload.type === "slot") {
            if (payload.slot === "A") {
                slotA = null;
            } else if (payload.slot === "B") {
                slotB = null;
            }
            renderSlots();
            setStatus("");

            const container = document.getElementById("palette");
            if (container) layoutPalette(container, container.children.length);
        }
    });
}

/*  Text-to-speech  */

async function speakColor(name) {
    try {
        const res = await fetch("/api/speak", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name }),
        });

        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            console.error(
                "TTS request failed:",
                res.status,
                err.detail || ""
            );
        }
    } catch (e) {
        console.error("TTS network error", e);
    }
}

/*  Mixing & palette    */

async function mix() {
    if (!slotA || !slotB) {
        setStatus("Pick two colors first.");
        return;
    }

    try {
        const res = await fetch("/api/mix", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ color_a: slotA, color_b: slotB }),
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

        // automatically clear the bowl after each successful mix
        clearBowl();
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

/*  Bootstrapping   */

document.addEventListener("DOMContentLoaded", () => {
    const mixBtn = document.getElementById("mixBtn");
    const clearBowlBtn = document.getElementById("clearBowlBtn");
    const clearPaletteBtn = document.getElementById("clearPaletteBtn");

    if (mixBtn) mixBtn.addEventListener("click", mix);
    if (clearBowlBtn) clearBowlBtn.addEventListener("click", clearBowl);
    if (clearPaletteBtn) clearPaletteBtn.addEventListener("click", clearPalette);

    setupBowlDropZones();
    setupPaletteDropZone();
    fetchPalette();
    renderSlots();

    // relayout on window resize without refetching server data
    window.addEventListener("resize", () => {
        const container = document.getElementById("palette");
        if (container) {
            const count = container.children.length ||
                (lastPaletteData ? Math.min(lastPaletteData.length, 20) : 0);
            layoutPalette(container, count);
        }
    });
});