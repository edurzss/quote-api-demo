# The base image
FROM python:3.10  
# Go into a folder within our docker image, where we can put our flask app
WORKDIR /src
COPY requirements.txt .
# Commands that run as an image
RUN pip install --no-cache-dir --upgrade -r requirements.txt   
# Copies the current local directory content into the WORKDIR inside image
COPY . .        
# Commands that run when container is run
CMD ["flask", "run", "--host", "0.0.0.0"]  