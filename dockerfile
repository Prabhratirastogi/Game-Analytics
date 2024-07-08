# Use the official Python image from the Docker Hub
FROM python:3.12.4

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . /app/


# Set the working directory to the subdirectory where manage.py is located
WORKDIR /app/game_analytics


# Make port 8000 available to the world outside this container
EXPOSE 8000

# Load environment variables from the .env file
COPY .env /app/.env

# Run Django server when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
