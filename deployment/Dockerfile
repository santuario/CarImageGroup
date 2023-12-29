FROM python:3.9-slim
FROM pytorch/pytorch:1.10.0-cuda11.3-cudnn8-runtime

WORKDIR /app

# Copy the contents of the "app" directory into the container
COPY app /app
COPY templates/ templates/

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
