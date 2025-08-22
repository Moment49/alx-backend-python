FROM python:3.10-alpine

# Set working directory inside the container
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update && apk add --no-cache python3-dev build-base mariadb-connector-c-dev pkgconfig

# Copy requirements and install dependencies
COPY requirements.txt /app/

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy all your app code into the container
COPY . /app/

# Expose the port your Django app runs on
EXPOSE 8000

# NOTE: -p is used when running the container, not inside the Dockerfile.
# Example: docker run -p 8000:8000 my-django-app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]