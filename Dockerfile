# Use the official Python image as the base image
FROM python:3.9-slim

# Install required system packages
RUN apt-get update && apt-get install -y software-properties-common
RUN dpkg --remove --force-remove-reinstreq python3-pip python3-setuptools python3-wheel

# Install PyTorch and related packages
RUN pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg &> /dev/null

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /app
COPY . /app
RUN bash ./scripts/download_models.sh


# Run download_models.sh script (assuming it's in the same directory as Dockerfile)



# Expose the port on which FastAPI is running (you can modify the port if needed)
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
