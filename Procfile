release: python manage.py migrate
web: daphne firealarm.asgi:application --port $PORT --bind 0.0.0.0 -v2
