FROM python:3.12-slim
WORKDIR /app

# Copy files
COPY requirements.txt .
COPY main.py .
COPY wsgi.py .
COPY static ./static

# Install dependencies
RUN pip install -r requirements.txt --upgrade

# Run the application
CMD ["python", "wsgi.py"]
