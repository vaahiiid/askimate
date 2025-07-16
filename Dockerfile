# Base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Collect static files (اختیاری ولی مفید برای Django)
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Start server using gunicorn
CMD ["gunicorn", "projectname.wsgi:application", "--bind", "0.0.0.0:8000"]



COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

# اجرای collectstatic برای جمع‌آوری استاتیک‌ها
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "AskiMate_platform.wsgi:application", "--bind", "0.0.0.0:8000"]
