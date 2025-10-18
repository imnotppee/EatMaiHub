#!/bin/bash

if [ "$1" == "frontend" ]; then
    echo "🔁 Switching to Flet 0.28.1 for frontend..."
    source frontend/venv/bin/activate
    pip uninstall -y flet
    pip install flet==0.28.1
    echo "✅ Done! Running frontend..."
    cd frontend
    python3 app.py
elif [ "$1" == "admin" ]; then
    echo "🔁 Switching to Flet 0.70.0.dev6281 for admin_dashboard..."
    source admin_dashboard/venv/bin/activate
    pip uninstall -y flet
    pip install flet==0.70.0.dev6281
    echo "✅ Done! Running admin_dashboard..."
    cd admin_dashboard
    python3 app.py
else
    echo "⚠️  Usage: ./switch_flet.sh [frontend|admin]"
fi
