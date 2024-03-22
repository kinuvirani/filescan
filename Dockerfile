# Use the official Python image as base
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN sudo apt-get update
RUN sudo apt-get install clamav

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port Flask will run on
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "u", "upload.py"]
