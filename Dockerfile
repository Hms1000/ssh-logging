# i use a python baseline image
FROM python:3.11-slim

# i setup a working directory
WORKDIR /app

# i copy dependencies to the container
COPY requirements.txt .

# i install dependencies to the container
RUN pip --no-cache-dependencies -r requirements.txt

# i then copy the rest of the file contents to the container from the source directory
COPY src/ .

CMD ["python3", "ssh-logging.py"]

