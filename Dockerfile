# Use Python 3.9 slim as the base image
FROM python:3.9-slim

# Install Node.js and npm
RUN apt-get update && apt-get install -y nodejs npm

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Install npm dependencies for Tailwind CSS
RUN npm install -D tailwindcss postcss autoprefixer

# Install Pillow
RUN pip install pillow

# Expose the port for the Django server
EXPOSE 8000

# Run migrations and start the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]