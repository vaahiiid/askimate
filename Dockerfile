FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

# اجرای collectstatic برای جمع‌آوری استاتیک‌ها
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "AskiMate_platform.wsgi:application", "--bind", "0.0.0.0:8000"]
