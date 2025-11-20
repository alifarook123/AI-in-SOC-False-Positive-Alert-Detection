# app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import csv

app = FastAPI(title="TXCr AI+SOC API", version="0.1.0")

# If you later add a web UI (React, etc.), allow it here:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = Path("data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/")
def health():
    return {"ok": True, "service": "txcr-ai-soc", "version": "0.1.0"}

@app.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a .csv file")

    target_path = DATA_DIR / file.filename
    content = await file.read()
    target_path.write_bytes(content)

    # Try to read header only (no numpy/pandas)
    try:
        header = []
        with target_path.open("r", newline="", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            header = next(reader, [])
    except Exception:
        header = []

    return {"saved_to": str(target_path), "columns": header, "bytes": len(content)}

@app.get("/files")
def list_files():
    files = [str(p.name) for p in DATA_DIR.glob("*.csv")]
    return {"count": len(files), "files": files}
