FROM python:3.10-alpine

# Set working directory inside the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your app code into the container
COPY . /app/

# Expose the port your Django app runs on
EXPOSE 8000

# Correct CMD syntax: separate arguments with commas
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]