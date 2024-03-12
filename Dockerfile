# Use an official Python runtime as a parent image
FROM python:3.8-bookworm

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN \
apt-get clean && apt-get update \
 && apt-get -y install libpq-dev gcc \
 && python3 -m pip install -r requirements.txt --no-cache-dir

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
