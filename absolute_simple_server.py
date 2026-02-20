#!/usr/bin/env python3
"""
САМЫЙ ПРОСТОЙ СЕРВЕР который точно заработает
"""

from fastapi import FastAPI
import os

app = FastAPI(title="Vega CRM", version="1.0.0")

@app.get("/")
async def root():
    return {
        "message": "🚀 Vega CRM работает!",
        "status": "OK",
        "version": "1.0.0",
        "timestamp": "2026-02-21T02:00:00Z"
    }

@app.get("/api/health")
async def health():
    return {"status": "healthy", "service": "vega-crm"}

@app.get("/api/objects")
async def objects():
    return {
        "objects": [
            {"id": 1, "name": "Резервуар РВС-5000", "status": "in_progress", "location": "Екатеринбург"},
            {"id": 2, "name": "Резервуар РГС-100", "status": "planning", "location": "Челябинск"},
            {"id": 3, "name": "Резервуар 50 000 м³", "status": "completed", "location": "Сабетта"}
        ],
        "count": 3,
        "total_budget": "30.45 млн руб."
    }

@app.get("/api/stats")
async def stats():
    return {
        "total_objects": 5,
        "completed": 1,
        "in_progress": 2,
        "planning": 2,
        "budget_total": "30.45 млн руб.",
        "budget_used": "25.5 млн руб."
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Запуск Vega CRM на порту {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
