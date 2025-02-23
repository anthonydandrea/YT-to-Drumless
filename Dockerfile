# Use an official Python image
FROM python:3.11

RUN apt-get update && apt-get install -y ffmpeg

# Set the working directory inside the container
WORKDIR /app

# Copy the project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
ENTRYPOINT ["python", "src/main.py"]

