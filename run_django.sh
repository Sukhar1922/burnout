#!/bin/bash

SESSION="django_proj"

if ! screen -ls | grep -q "$SESSION"; then
  echo "Стартуем"
  screen -dmS "$SESSION" bash -c "
    source venv/bin/activate;
    cd server;
    python3.12 manage.py runserver 0.0.0.0:82;
    exec bash
  "
else
  echo "Уже есть сессия screen $SESSION"
fi