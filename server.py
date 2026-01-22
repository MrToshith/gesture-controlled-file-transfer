from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Mount current directory to serve pfp.png
app.mount("/images", StaticFiles(directory="."), name="images")

templates = Jinja2Templates(directory="templates")

# Simple state to store image display status
transfer_state = {
    "status": "idle", # idle, grabbed, transferred
    "image_url": "/images/pfp.png"
}

class TransferRequest(BaseModel):
    action: str # "grab" or "release"

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/status")
async def get_status():
    return transfer_state

@app.post("/transfer")
async def trigger_transfer(req: TransferRequest):
    global transfer_state
    if req.action == "grab":
        transfer_state["status"] = "grabbed"
    elif req.action == "release":
        transfer_state["status"] = "transferred"
    elif req.action == "reset":
        transfer_state["status"] = "idle"
        
    return {"status": "ok", "state": transfer_state}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)