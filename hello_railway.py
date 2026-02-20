#!/usr/bin/env python3
"""
HELLO RAILWAY - самая простая версия которая точно заработает
"""

# Минимальный код - ничего лишнего
from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "status": "OK", 
        "message": "🚀 Vega CRM работает на Railway!",
        "version": "1.0.0",
        "timestamp": "2026-02-21T02:05:00Z"
    }

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "vega-crm"}

@app.get("/api/objects")
def get_objects():
    return {
        "objects": [
            {"id": 1, "name": "Резервуар РВС-5000", "status": "active"},
            {"id": 2, "name": "Резервуар РГС-100", "status": "planning"}
        ]
    }

@app.get("/docs")
def get_docs():
    return {
        "endpoints": [
            {"path": "/", "method": "GET", "description": "Главная страница"},
            {"path": "/api/health", "method": "GET", "description": "Проверка здоровья"},
            {"path": "/api/objects", "method": "GET", "description": "Список объектов"}
        ]
    }

if __name__ == "__main__":
    # Получаем порт от Railway или используем 8000
    port = int(os.environ.get("PORT", 8000))
    
    print("=" * 60)
    print("🚀 HELLO RAILWAY - Vega CRM")
    print("=" * 60)
    print(f"Порт: {port}")
    print("Запускаю сервер...")
    print("=" * 60)
    
    # Запускаем сервер
    uvicorn.run(app, host="0.0.0.0", port=port)

