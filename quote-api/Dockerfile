# Python base image
FROM python:3.10  
# Create a folder within our docker image, where we can copy our flask app
WORKDIR /src
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt   
# Copies the current local directory content into the WORKDIR inside image
COPY . .        
# Commands that run when container starts
ENTRYPOINT ["gunicorn", "--workers=1", "--bind", "0.0.0.0:5000", "app:create_app()", "--reload"]
# ENTRYPOINT ["flask", "run", "--host", "0.0.0.0"]  