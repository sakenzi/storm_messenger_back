import uvicorn

if __name__ == "__main__":
    # uvicorn.run("main:app", host="172.20.10.3", port=8000, reload=True)
    # uvicorn.run("main:app", host="172.20.10.14", port=8000, reload=True)
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    # uvicorn.run("main:app", host="172.20.10.5", port=8000, reload=True)
    # uvicorn.run("main:app", host="192.168.152.118", port=8000, reload=True)
    # uvicorn.run("main:app", host="169.254.144.185", port=8000, reload=True)
