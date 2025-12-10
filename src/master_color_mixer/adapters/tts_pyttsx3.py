import threading
import logging
from typing import Optional

import pyttsx3  # uses SAPI5 on Windows

logger = logging.getLogger(__name__)

def _speak_worker(text: str, rate: int) -> None:
    # initialize a new TTS engine in this thread
    engine: Optional[pyttsx3.Engine] = None
    try:
        logger.debug("TTS worker starting for text=%r", text)
        engine = pyttsx3.init()  # new COM/SAPI engine in this thread
        try:
            engine.setProperty("rate", rate) # attempt to set rate (per minute)
        except Exception as e:
            logger.warning("Could not set TTS rate: %s", e)

        engine.say(text) # queue the text
        engine.runAndWait() # blocking wait until all queued commands are processed
        logger.debug("TTS worker finished for text=%r", text)
    except Exception as e:
        logger.exception("Error in TTS worker: %s", e)
    finally:
        # ensure engine is stopped to release resources
        if engine is not None:
            try:
                engine.stop()
            except Exception:
                pass # ignore errors on stop

def speak(text: str, rate: int = 160) -> None:
    if not text:
        return

    logger.info("Queueing TTS for %r", text)
    t = threading.Thread(
        target=_speak_worker,
        args=(text, rate),
        daemon=True, # daemon threads exit automatically when the main program exits
    )
    t.start()

def speak_color_name(name: str) -> None:
    logger.info("speak_color_name(%r) called", name)
    speak(name)

def shutdown(wait: bool = True, join_timeout: float = 2.0) -> None:
    logger.info("tts_pyttsx3.shutdown() called (nothing to clean up)")