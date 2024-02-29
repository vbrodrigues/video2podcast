FROM python:3.10

# Set the working directory in the container
WORKDIR /app

ENV HOSTNAME "0.0.0.0"

RUN apt-get update && apt-get install -y ffmpeg

COPY /src .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8080

# Command to run on container start
CMD [ "uvicorn", "app:app", "--host", "0.0.0.0" , "--port", "8080"]