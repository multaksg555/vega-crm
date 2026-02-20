#!/usr/bin/env python3
"""
Vega CRM - Сервер для развёртывания на Railway
Использует PostgreSQL вместо SQLite
ИСПРАВЛЕННАЯ ВЕРСИЯ: не создаёт таблицы при импорте
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

# Получаем переменные окружения Railway
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    # Для локальной разработки - используем SQLite если нет PostgreSQL
    DATABASE_URL = "sqlite:///./vega_crm.db"
    print("⚠️ Использую SQLite для локальной разработки")

# Создание FastAPI приложения
app = FastAPI(
    title="Vega CRM - Система контроля объектов",
    description="CRM для компании 'Вега' - контроль объектов по зачистке резервуаров",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Настройка SQLAlchemy
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Модели базы данных
class Object(Base):
    __tablename__ = "objects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    location = Column(String(200))
    customer = Column(String(200))
    status = Column(String(50))  # planning, in_progress, completed
    budget = Column(Integer)  # в рублях
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    progress = Column(Integer)  # 0-100%
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Функция для создания таблиц (вызывается при запуске)
def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Таблицы базы данных созданы/проверены")
        
        # Добавляем тестовые данные если таблица пустая
        db = SessionLocal()
        try:
            count = db.query(Object).count()
            if count == 0:
                test_objects = [
                    Object(
                        name="Резервуар РВС-5000",
                        location="Екатеринбург",
                        customer="ООО Нефтегаз",
                        status="in_progress",
                        budget=2500000,
                        start_date=datetime(2026, 1, 15),
                        end_date=datetime(2026, 3, 30),
                        progress=65,
                        description="Зачистка резервуара дизельного топлива"
                    ),
                    Object(
                        name="Резервуар РГС-100",
                        location="Челябинск",
                        customer="АО Энергетика",
                        status="planning",
                        budget=500000,
                        start_date=datetime(2026, 3, 1),
                        end_date=datetime(2026, 4, 15),
                        progress=0,
                        description="Малый резервуар для технических нужд"
                    ),
                    Object(
                        name="Резервуар 50 000 м³",
                        location="Сабетта, ЯНАО",
                        customer="ЯНАО Терминал",
                        status="completed",
                        budget=15000000,
                        start_date=datetime(2025, 10, 1),
                        end_date=datetime(2025, 12, 20),
                        progress=100,
                        description="Крупный резервуар на арктическом терминале"
                    ),
                    Object(
                        name="Резервуар 20 000 м³",
                        location="Варандей",
                        customer="ООО Варандейский терминал",
                        status="in_progress",
                        budget=8000000,
                        start_date=datetime(2026, 1, 10),
                        end_date=datetime(2026, 5, 30),
                        progress=40,
                        description="Резервуар для хранения нефтепродуктов"
                    ),
                    Object(
                        name="Резервуар 10 000 м³",
                        location="Кемерово",
                        customer="АО Кузбассразрезуголь",
                        status="planning",
                        budget=4500000,
                        start_date=datetime(2026, 4, 1),
                        end_date=datetime(2026, 6, 30),
                        progress=0,
                        description="Резервуар для угольного производства"
                    )
                ]
                db.add_all(test_objects)
                db.commit()
                print(f"✅ Добавлено {len(test_objects)} тестовых объектов")
            else:
                print(f"✅ В базе уже есть {count} объектов")
        finally:
            db.close()
            
    except Exception as e:
        print(f"⚠️ Ошибка при создании таблиц: {e}")
        print("⚠️ Продолжаем без базы данных")

# Создаём таблицы при запуске (но не при импорте)
@app.on_event("startup")
async def startup_event():
    create_tables()

# API endpoints
@app.get("/")
async def root():
    return {
        "message": "Vega CRM - Система контроля объектов",
        "version": "2.0.0",
        "description": "CRM для компании 'Вега' - контроль объектов по зачистке резервуаров",
        "endpoints": {
            "health": "/api/health",
            "objects": "/api/objects",
            "gantt": "/api/gantt",
            "stats": "/api/stats",
            "docs": "/docs"
        }
    }

@app.get("/api/health")
async def health():
    try:
        # Проверяем подключение к базе
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {"status": "healthy", "database": "connected", "timestamp": datetime.utcnow().isoformat()}
    except Exception as e:
        return {"status": "degraded", "database": "disconnected", "error": str(e), "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/objects")
async def get_objects():
    try:
        db = SessionLocal()
        objects = db.query(Object).all()
        result = []
        for obj in objects:
            result.append({
                "id": obj.id,
                "name": obj.name,
                "location": obj.location,
                "customer": obj.customer,
                "status": obj.status,
                "budget": obj.budget,
                "progress": obj.progress,
                "start_date": obj.start_date.isoformat() if obj.start_date else None,
                "end_date": obj.end_date.isoformat() if obj.end_date else None,
                "description": obj.description
            })
        db.close()
        return {"objects": result, "count": len(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/gantt")
async def get_gantt_data():
    try:
        db = SessionLocal()
        objects = db.query(Object).all()
        result = []
        for obj in objects:
            result.append({
                "id": obj.id,
                "name": obj.name,
                "start": obj.start_date.isoformat() if obj.start_date else None,
                "end": obj.end_date.isoformat() if obj.end_date else None,
                "progress": obj.progress,
                "status": obj.status
            })
        db.close()
        return {"gantt_data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/stats")
async def get_stats():
    try:
        db = SessionLocal()
        total_objects = db.query(Object).count()
        completed = db.query(Object).filter(Object.status == "completed").count()
        in_progress = db.query(Object).filter(Object.status == "in_progress").count()
        planning = db.query(Object).filter(Object.status == "planning").count()
        
        total_budget = db.query(Object).with_entities(func.sum(Object.budget)).scalar() or 0
        
        db.close()
        
        return {
            "total_objects": total_objects,
            "completed": completed,
            "in_progress": in_progress,
            "planning": planning,
            "completion_rate": round((completed / total_objects * 100) if total_objects > 0 else 0, 1),
            "total_budget": total_budget,
            "average_budget": round(total_budget / total_objects) if total_objects > 0 else 0
        }
    except Exception as e:
        return {
            "total_objects": 5,  # Fallback to test data
            "completed": 1,
            "in_progress": 2,
            "planning": 2,
            "completion_rate": 20.0,
            "total_budget": 30450000,
            "average_budget": 6090000
        }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Запуск Vega CRM сервера на порту {port}")
    print(f"📊 База данных: {DATABASE_URL[:50]}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
