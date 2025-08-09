# Use Python 3.10 base image
FROM python:3.10-bookworm

# Set working directory inside the container
WORKDIR /app

# Copy backend code
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
