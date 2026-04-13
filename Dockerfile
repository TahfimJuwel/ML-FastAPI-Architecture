# 1. Base Image: Start with an official, lightweight Linux computer that already has Python 3.11 installed
FROM python:3.11-slim

# 2. Set the "Working Directory" inside the container
WORKDIR /code

# 3. Copy the library blueprint first
COPY ./requirements.txt /code/requirements.txt

# 4. Install the libraries inside the container
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 5. Copy the rest of our actual code into the container
COPY ./app /code/app

# 6. Open Port 8000 on the container so traffic can get inside
EXPOSE 8000

# 7. The command to start the server when the container turns on
# Note the space after CMD
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]