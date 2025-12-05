
import threading, time, webbrowser, uvicorn

def _open_browser_with_delay(url: str, delay: float = 1.0) -> None:

    def _target():
        time.sleep(delay)
        try:
            webbrowser.open(url)
        except Exception:
            # if browser cannot open, program does not crash
            pass

    t = threading.Thread(target=_target, daemon=True)
    t.start()

def main() -> None:
    url = "http://127.0.0.1:8000" # local on port 8000
    _open_browser_with_delay(url)
    # loading from the current package
    uvicorn.run("master_color_mixer.app:app", host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
    main()