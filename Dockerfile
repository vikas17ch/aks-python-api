# 1. Use an official Python runtime as a parent image
FROM python:3.9-slim

# 2. Set the working directory in the container
WORKDIR /app

# 3. Copy the requirements file first (for faster caching)
COPY requirements.txt .

# 4. Install FastAPI, Uvicorn, PostgreSQL drivers, and aiofiles
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the static folder (The UI)
# This creates /app/static/ inside the container
COPY static/ /app/static/

# 6. Copy the application code
# This creates /app/app/main.py inside the container
COPY app/ /app/app/

# 7. Open port 8000 for the API
EXPOSE 8000

# 8. Start the server
# We tell uvicorn to look in 'app.main' for the 'app' object
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]