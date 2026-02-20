#!/usr/bin/env python3
"""
СУПЕР ПРОСТОЙ СЕРВЕР который точно заработает на Railway
"""

from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Vega CRM работает!", "status": "OK"}

@app.get("/api/health")
async def health():
    return {"status": "healthy", "service": "vega-crm"}

@app.get("/api/objects")
async def objects():
    return {
        "objects": [
            {"id": 1, "name": "Резервуар РВС-5000", "status": "in_progress"},
            {"id": 2, "name": "Резервуар РГС-100", "status": "planning"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Запуск простого сервера на порту {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
