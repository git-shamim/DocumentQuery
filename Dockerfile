FROM python:3.10-slim

# Set environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create app directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Run Streamlit with relaxed CORS and XSRF protection (allows iframe embedding)
CMD ["streamlit", "run", "app.py", \
     "--server.port=8080", \
     "--server.address=0.0.0.0", \
     "--server.enableCORS=false", \
     "--server.enableXsrfProtection=false", \
     "--server.enableWebsocketCompression=false", \
     "--server.headless=true"]
