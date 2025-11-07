# Running this module starts the FastAPI app and prints a hello message.

import uvicorn

def main():
    print("Hello MasterColorMixer (starting API...)")
    uvicorn.run("mastercolormixer.app:app", host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
    main()