# Base image
FROM python:3.9

LABEL agusrichard "nguyen.duc.sang@tanaakk.com"

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies including libgl1-mesa-glx for OpenGL support
RUN apt-get update \
    && apt-get install -y libgl1-mesa-glx \
    && apt-get clean

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]