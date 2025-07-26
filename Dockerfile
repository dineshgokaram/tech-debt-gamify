# Dockerfile

# 1. Start with an official Python base image.
FROM python:3.11-slim

# 2. Set the working directory inside the container.
WORKDIR /app

# 3. --- NEW STEP: Install git into the container's operating system ---
# First, update the package lists, then install git without extra packages.
# The '-y' flag automatically confirms the installation.
RUN apt-get update && apt-get install -y git --no-install-recommends

# 4. Copy the requirements file into the container.
COPY ./requirements.txt /app/requirements.txt

# 5. Install the Python dependencies.
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 6. Copy the rest of your application code into the container.
COPY ./app /app