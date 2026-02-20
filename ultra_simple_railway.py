#!/usr/bin/env python3
"""
ULTRA SIMPLE RAILWAY - минимальный код который точно заработает
"""

from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "OK",
        "message": "🚀 Vega CRM работает на Railway!",
        "version": "1.0.0",
        "timestamp": "2026-02-21T02:32:00Z"
    })

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy", "service": "vega-crm"})

@app.route('/api/objects')
def objects():
    return jsonify({
        "objects": [
            {"id": 1, "name": "Резервуар РВС-5000", "status": "active"},
            {"id": 2, "name": "Резервуар РГС-100", "status": "planning"}
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"🚀 ULTRA SIMPLE сервер запущен на порту {port}")
    app.run(host='0.0.0.0', port=port)
