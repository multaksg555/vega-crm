#!/usr/bin/env python3
"""
Vega CRM - Сервер для развёртывания на Railway
Использует PostgreSQL вместо SQLite
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
    # Для локальной разработки
    DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/vega_crm"

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
    client_name = Column(String(200), nullable=False)
    location = Column(String(200), nullable=False)
    status = Column(String(50), default="planning")
    description = Column(Text, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    budget = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DailyReport(Base):
    __tablename__ = "daily_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    object_id = Column(Integer, nullable=False)
    work_description = Column(Text, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(100), nullable=True)

class GanttItem(Base):
    __tablename__ = "gantt_items"
    
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String(200), nullable=False)
    start_date = Column(String(50), nullable=False)
    end_date = Column(String(50), nullable=False)
    progress = Column(Integer, default=0)
    color = Column(String(20), default="#3498db")
    object_id = Column(Integer, nullable=True)

# Создаем таблицы
Base.metadata.create_all(bind=engine)

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Функция для инициализации тестовых данных
def init_test_data():
    db = SessionLocal()
    
    try:
        # Проверяем есть ли уже данные
        count = db.query(Object).count()
        if count == 0:
            # Добавляем тестовые объекты
            test_objects = [
                Object(
                    name="Резервуар РВС-5000",
                    client_name="ООО Нефтегаз",
                    location="Екатеринбург",
                    status="in_progress",
                    description="Зачистка резервуара 5000 м³ для хранения дизельного топлива",
                    budget=2500000
                ),
                Object(
                    name="Резервуар РГС-100",
                    client_name="АО Энергетика",
                    location="Челябинск",
                    status="planning",
                    description="Зачистка резервуара 100 м³ на АЗС",
                    budget=500000
                ),
                Object(
                    name="Резервуар 50 000 м³",
                    client_name="ЯНАО Терминал",
                    location="Сабетта",
                    status="completed",
                    description="Зачистка крупного резервуара в аэропорту Сабетта",
                    budget=15000000
                ),
                Object(
                    name="Резервуар 20 000 м³",
                    client_name="ООО Варандейский терминал",
                    location="Варандей",
                    status="in_progress",
                    description="Зачистка резервуаров для светлых нефтепродуктов",
                    budget=8000000
                ),
                Object(
                    name="Резервуар 10 000 м³",
                    client_name="АО Кузбассразрезуголь",
                    location="Кемерово",
                    status="planning",
                    description="Зачистка резервуаров складов ГСМ",
                    budget=4500000
                )
            ]
            
            db.add_all(test_objects)
            db.commit()
            
            # Добавляем тестовые данные для диаграммы Ганта
            test_gantt = [
                GanttItem(
                    task="Резервуар РВС-5000",
                    start_date="2026-02-20",
                    end_date="2026-02-25",
                    progress=60,
                    color="#3498db",
                    object_id=1
                ),
                GanttItem(
                    task="Резервуар РГС-100",
                    start_date="2026-02-22",
                    end_date="2026-02-28",
                    progress=20,
                    color="#2ecc71",
                    object_id=2
                ),
                GanttItem(
                    task="Резервуар 50 000 м³",
                    start_date="2026-02-15",
                    end_date="2026-02-20",
                    progress=100,
                    color="#e74c3c",
                    object_id=3
                ),
                GanttItem(
                    task="Резервуар 20 000 м³",
                    start_date="2026-02-21",
                    end_date="2026-03-05",
                    progress=40,
                    color="#9b59b6",
                    object_id=4
                ),
                GanttItem(
                    task="Резервуар 10 000 м³",
                    start_date="2026-02-25",
                    end_date="2026-03-10",
                    progress=10,
                    color="#f39c12",
                    object_id=5
                )
            ]
            
            db.add_all(test_gantt)
            db.commit()
            
            print("✅ Тестовые данные инициализированы")
    except Exception as e:
        print(f"❌ Ошибка инициализации данных: {e}")
    finally:
        db.close()

# Инициализируем данные при старте
init_test_data()

# API endpoints
@app.get("/")
async def root():
    return {
        "message": "🚀 Vega CRM API работает!",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "deployment": "Railway",
        "endpoints": [
            "/docs - Документация API",
            "/api/health - Проверка здоровья",
            "/api/objects - Все объекты",
            "/api/objects/{id} - Конкретный объект",
            "/api/gantt - Данные для диаграммы Ганта",
            "/api/stats - Статистика",
            "/api/environment - Информация о развёртывании"
        ]
    }

@app.get("/api/health")
async def health_check():
    db = SessionLocal()
    try:
        # Проверяем соединение с базой данных
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"error: {str(e)}"
    finally:
        db.close()
    
    return {
        "status": "healthy",
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat(),
        "environment": os.environ.get("RAILWAY_ENVIRONMENT", "development")
    }

@app.get("/api/objects")
async def get_objects():
    db = SessionLocal()
    try:
        objects = db.query(Object).order_by(Object.created_at.desc()).all()
        
        result = []
        for obj in objects:
            result.append({
                "id": obj.id,
                "name": obj.name,
                "client_name": obj.client_name,
                "location": obj.location,
                "status": obj.status,
                "description": obj.description,
                "budget": obj.budget,
                "created_at": obj.created_at.isoformat() if obj.created_at else None,
                "updated_at": obj.updated_at.isoformat() if obj.updated_at else None
            })
        
        return result
    finally:
        db.close()

@app.get("/api/objects/{object_id}")
async def get_object(object_id: int):
    db = SessionLocal()
    try:
        obj = db.query(Object).filter(Object.id == object_id).first()
        
        if not obj:
            raise HTTPException(status_code=404, detail="Object not found")
        
        return {
            "id": obj.id,
            "name": obj.name,
            "client_name": obj.client_name,
            "location": obj.location,
            "status": obj.status,
            "description": obj.description,
            "budget": obj.budget,
            "created_at": obj.created_at.isoformat() if obj.created_at else None,
            "updated_at": obj.updated_at.isoformat() if obj.updated_at else None
        }
    finally:
        db.close()

@app.get("/api/gantt")
async def get_gantt_data():
    db = SessionLocal()
    try:
        items = db.query(GanttItem).all()
        
        result = []
        for item in items:
            result.append({
                "id": item.id,
                "task": item.task,
                "start": item.start_date,
                "end": item.end_date,
                "progress": item.progress,
                "color": item.color,
                "object_id": item.object_id
            })
        
        return result
    finally:
        db.close()

@app.get("/api/stats")
async def get_stats():
    db = SessionLocal()
    try:
        total_objects = db.query(Object).count()
        completed_objects = db.query(Object).filter(Object.status == "completed").count()
        in_progress_objects = db.query(Object).filter(Object.status == "in_progress").count()
        planning_objects = db.query(Object).filter(Object.status == "planning").count()
        
        total_budget = db.query(Object).filter(Object.budget.isnot(None)).all()
        total_budget_sum = sum([obj.budget for obj in total_budget if obj.budget])
        
        return {
            "total_objects": total_objects,
            "completed": completed_objects,
            "in_progress": in_progress_objects,
            "planning": planning_objects,
            "total_budget": total_budget_sum,
            "average_budget": round(total_budget_sum / total_objects) if total_objects > 0 else 0,
            "completion_rate": round((completed_objects / total_objects * 100) if total_objects > 0 else 0, 1)
        }
    finally:
        db.close()

@app.get("/api/environment")
async def get_environment():
    return {
        "railway_environment": os.environ.get("RAILWAY_ENVIRONMENT"),
        "railway_project_id": os.environ.get("RAILWAY_PROJECT_ID"),
        "railway_service_id": os.environ.get("RAILWAY_SERVICE_ID"),
        "database_url": "configured" if os.environ.get("DATABASE_URL") else "not configured",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/objects")
async def create_object(object_data: dict):
    db = SessionLocal()
    try:
        new_object = Object(
            name=object_data.get("name"),
            client_name=object_data.get("client_name"),
            location=object_data.get("location"),
            status=object_data.get("status", "planning"),
            description=object_data.get("description"),
            budget=object_data.get("budget")
        )
        
        db.add(new_object)
        db.commit()
        db.refresh(new_object)
        
        return {
            "message": "Object created successfully",
            "object_id": new_object.id,
            "object": {
                "id": new_object.id,
                "name": new_object.name,
                "client_name": new_object.client_name,
                "location": new_object.location,
                "status": new_object.status
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    
    print("=" * 60)
    print("🚀 Vega CRM - Запуск на Railway")
    print("=" * 60)
    print(f"📊 Версия: 2.0.0")
    print(f"🌐 Порт: {port}")
    print(f"🗄️ База данных: {'PostgreSQL (Railway)' if os.environ.get('DATABASE_URL') else 'SQLite (локально)'}")
    print(f"📱 API endpoints доступны по адресу: http://localhost:{port}")
    print(f"📚 Документация: http://localhost:{port}/docs")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")