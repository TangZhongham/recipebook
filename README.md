# Recipe Book Application

- [Project Overview](#project-overview)
- [Code Structure](#code-structure)
- [Features](#features)
- [Deployment](#deployment)
- [Instructions for Running the Application](#instructions-for-running-the-application)
- [Dependencies](#dependencies)

--------------------------------------------------------------------------------------------------------------
## Project Overview
The Recipe Book Application is a web-based platform that allows users to create, view and manage recipes.
Users can follow other users, view their recipe feed, and interact with recipes by liking or favoriting them.
The application is built using Django for the backed, SQLite for the database and Tailwind CSS for styling.

--------------------------------------------------------------------------------------------------------------
## Code Structure
The project is organized into the following directories and files:

### **Project Root**
1. '.venv'/ : Virtual environment for managing dependencies.
2. 'recipebook/ : Contains project-level configuration files.
    - 'settings.py' : Django settings for the project.
    - 'urls.py' : URL configiration for the project.
3. 'recipe_web/' : Main application folder containing all app-specific logic.
   - 'templates/' : HTML templates for rendering views.
     - 'recipe_web/' : Contains templates like 'home.html', 'base.html', 'user_profile.html' etc.
     - 'registration/' : Contains templates for user authentication like 'login.html'
   - 'views.py' : Contains view functions that handle HTTP requests and responses.
   - 'models.py' : Defines database models.
   - 'urls.py' : App-specific URL configuration.
4. 'media/' : Stores uploaded media files such as profile pictures and recipe images.

-------------------------------------------------------------------------------------------------------
## Features
1. User registration and authentication.
2. Recipe creation, editing and deletion.
3. Viewing a list of recipes.
4. User profile management with profile pictures.
5. User interaction eg. following and unfollowing other authors.
6. User interations eg. 'like' and 'unfavorite' recipes 
6. Add search functionality for recipes.
7. Implement filtering options eg. by 'Cuisine Types' and 'Dietary Types'.

-------------------------------------------------------------------------------------------------------------
## Deployment

### Overview
This section provides instructions to deploy the **Recipe Book Application** using Docker, allowing you to run the application in a containerized environment.

### Prerequisites
- Docker installed on your machine ([Download Docker](https://www.docker.com/))
- Ensure the project files are cloned and available in the current directory

### Steps

#### 1. Build the Docker Image

Build the Docker image using the provided `Dockerfile`:

```bash
docker build -t recipebook .
```

#### 2. Run the Docker Container

Start a container from the built image, mapping port 8000 on your host to port 8000 in the container:

```bash
docker run -d -p 8000:8000 recipebook
```

The -d flag runs the container in detached mode, and -p 8000:8000 ensures the application is accessible at http://localhost:8000/.

-------------------------------------------------------------------------------------------------------------
## Instructions for Running the Application

### **Step 1: Clone the Repository**
- Clone this repository to your local machine:
    git clone https://github.com/TangZhongham/recipebook.git

### **Step 2: Set Up Virtual Environment**
- Navigate to the project directory and set up a virtual environment:
    python -m venv .venv
- Activate the virtual environment:
    .venv\Scripts\activate

### **Step 3: Install Dependencies**
- Install the requied Python packages from 'requirements.txt':
    pip install -r requirements.txt
- Install Tailwind CSS dependencies:
    npm install -D tailwindcss postcss autoprefixer 
- Install additional library for Python Imaging Library
    pip install pillow

### **Step 4: Apply MIgrations**
- Apply database migrations to set up the SQLite database:
    python manage.py makemigrations
    python manage.py migrate

### **Step 5: Run the Development Server**
- Start the Django development server:
    python manage.py runserver

### **Step 6: Access the recipe book application in your browser
- Go to http://127.0.0.1:8000/ and you should see the homepage "Welcome to Recipe Hub".

-------------------------------------------------------------------------------------------------------
## Dependencies

### Python Packages:
- Django : Web Framework for building the application backend.
- SQLite : Lightweight database used for development.
- Pillow : Python Imaging Library for image processing.

### CSS Tools
- Tailwind CSS: Utility-first CSS framework for styling.



        