#!/usr/bin/env python3
"""
ULTRA SIMPLE SERVER - самый простой вариант который точно заработает
"""

from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()

@app.get("/")
def root():
    return {"status": "OK", "message": "Vega CRM работает!", "version": "1.0.0"}

@app.get("/api/health")
def health():
    return {"status": "healthy", "service": "vega-crm"}

@app.get("/api/objects")
def objects():
    return {
        "objects": [
            {"id": 1, "name": "Резервуар РВС-5000", "status": "active"},
            {"id": 2, "name": "Резервуар РГС-100", "status": "planning"}
        ]
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 ULTRA SIMPLE Vega CRM запущен на порту {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
