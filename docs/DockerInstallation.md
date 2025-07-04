# install
```bash

* sudo apt install apt-transport-https ca-certificates curl software-properties-common
* curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
* echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
* sudo apt update






```

```bash



echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null


```


## install docker
``bash
* sudo apt install docker-ce docker-ce-cli containerd.io

もしエラーがある場合には

【sudo rm /usr/share/keyrings/docker-archive-keyring.gpg
】
【sudo rm /etc/apt/sources.list.d/docker.list
】
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg


echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null


sudo apt update

sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin

```

## After installation, verify

```bash
* docker --version

* docker compose version

* docker run hello-word


```


# PostgreSQL with Docker + Django for Beginners

A complete step-by-step guide to set up PostgreSQL with Docker and Django for your ReserveIt app.

## Why Use Docker with PostgreSQL?

- **Easy Setup**: No need to install PostgreSQL directly on your system
- **Consistent Environment**: Same database setup across all developers
- **Isolation**: Database runs in its own container
- **Easy Cleanup**: Remove containers when done

## Prerequisites

- Docker Desktop installed and running
- Python 3.8+ installed
- Basic knowledge of Django

## Step 1: Create Docker Files

### 1.1 Create `docker-compose.yml`

Create this file in your project root:

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  db:
    image: postgres:15
    container_name: reserveit_db
    environment:
      POSTGRES_DB: reserveit_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: mypassword123
      POSTGRES_HOST_AUTH_METHOD: trust
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    restart: unless-stopped

  # Django Web Application
  web:
    build: .
    container_name: reserveit_web
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://postgres:mypassword123@db:5432/reserveit_db

volumes:
  postgres_data:
```

### 1.2 Create `Dockerfile`

Create this file in your project root:

```dockerfile
# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        gcc \
        python3-dev \
        musl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### 1.3 Create `requirements.txt`

```txt
Django==4.2.7
psycopg2-binary==2.9.9
python-decouple==3.8
djangorestframework==3.14.0
django-cors-headers==4.3.1
Pillow==10.0.1
```

## Step 2: Configure Django Settings

### 2.1 Create `.env` file

```env
# Database
DATABASE_URL=postgresql://postgres:mypassword123@localhost:5432/reserveit_db
DB_NAME=reserveit_db
DB_USER=postgres
DB_PASSWORD=mypassword123
DB_HOST=localhost
DB_PORT=5432

# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 2.2 Update `settings.py`

```python
import os
from decouple import config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='your-fallback-secret-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    # Your apps
    'memos',
    'reservations',  # Add your apps here
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'your_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'your_project.wsgi.application'

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='reserveit_db'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default='mypassword123'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True
```

## Step 3: Running the Application

### 3.1 Start PostgreSQL Only (for development)

```bash
# Start only the database
docker-compose up db -d

# Check if it's running
docker-compose ps
```

### 3.2 Run Django Locally (connecting to Docker PostgreSQL)

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### 3.3 Run Everything with Docker

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

## Step 4: Useful Docker Commands

### 4.1 Basic Commands

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs

# View specific service logs
docker-compose logs web
docker-compose logs db
```

### 4.2 Database Management

```bash
# Connect to PostgreSQL container
docker-compose exec db psql -U postgres -d reserveit_db

# Run Django migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Django shell
docker-compose exec web python manage.py shell
```

### 4.3 Cleanup Commands

```bash
# Stop and remove containers
docker-compose down

# Remove containers and volumes
docker-compose down -v

# Remove everything including images
docker-compose down --rmi all -v
```

## Step 5: Testing the Setup

### 5.1 Check Database Connection

Create a simple test file `test_db.py`:

```python
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from django.db import connection

def test_database_connection():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"Database connection successful: {result}")
    except Exception as e:
        print(f"Database connection failed: {e}")

if __name__ == "__main__":
    test_database_connection()
```

Run: `python test_db.py`

### 5.2 Create Sample Models

In your `memos/models.py`:

```python
from django.db import models
from django.contrib.auth.models import User

class Memo(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Reservation(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.start_time}"
```

## Step 6: Common Issues and Solutions

### 6.1 Database Connection Errors

**Problem**: `connection to server at "localhost" (127.0.0.1), port 5432 failed`

**Solution**:
```bash
# Check if PostgreSQL container is running
docker-compose ps

# Restart the database
docker-compose restart db
```

### 6.2 Migration Issues

**Problem**: `relation "django_migrations" does not exist`

**Solution**:
```bash
# Reset migrations
docker-compose exec web python manage.py migrate --run-syncdb
```

### 6.3 Permission Errors

**Problem**: Permission denied errors in Docker

**Solution**:
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

## Step 7: Production Tips

### 7.1 Environment Variables

Use separate `.env` files for different environments:
- `.env.development`
- `.env.production`

### 7.2 Database Backups

```bash
# Create backup
docker-compose exec db pg_dump -U postgres reserveit_db > backup.sql

# Restore backup
docker-compose exec -T db psql -U postgres reserveit_db < backup.sql
```

### 7.3 Security Considerations

- Use strong passwords
- Don't commit `.env` files
- Use environment-specific settings
- Enable SSL in production

## Next Steps

1. **Add your Django apps** (memos, reservations)
2. **Create API endpoints** with Django REST Framework
3. **Connect with React frontend**
4. **Add authentication** and user management
5. **Implement reservation logic**
6. **Add tests** for your applications

This setup gives you a solid foundation for developing your ReserveIt app with PostgreSQL and Django using Docker!# PostgreSQL with Docker + Django for Beginners

A complete step-by-step guide to set up PostgreSQL with Docker and Django for your ReserveIt app.

## Why Use Docker with PostgreSQL?

- **Easy Setup**: No need to install PostgreSQL directly on your system
- **Consistent Environment**: Same database setup across all developers
- **Isolation**: Database runs in its own container
- **Easy Cleanup**: Remove containers when done

## Prerequisites

- Docker Desktop installed and running
- Python 3.8+ installed
- Basic knowledge of Django

## Step 1: Create Docker Files

### 1.1 Create `docker-compose.yml`

Create this file in your project root:

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  db:
    image: postgres:15
    container_name: reserveit_db
    environment:
      POSTGRES_DB: reserveit_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: mypassword123
      POSTGRES_HOST_AUTH_METHOD: trust
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    restart: unless-stopped

  # Django Web Application
  web:
    build: .
    container_name: reserveit_web
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://postgres:mypassword123@db:5432/reserveit_db

volumes:
  postgres_data:
```

### 1.2 Create `Dockerfile`

Create this file in your project root:

```dockerfile
# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        gcc \
        python3-dev \
        musl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### 1.3 Create `requirements.txt`

```txt
Django==4.2.7
psycopg2-binary==2.9.9
python-decouple==3.8
djangorestframework==3.14.0
django-cors-headers==4.3.1
Pillow==10.0.1
```

## Step 2: Configure Django Settings

### 2.1 Create `.env` file

```env
# Database
DATABASE_URL=postgresql://postgres:mypassword123@localhost:5432/reserveit_db
DB_NAME=reserveit_db
DB_USER=postgres
DB_PASSWORD=mypassword123
DB_HOST=localhost
DB_PORT=5432

# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 2.2 Update `settings.py`

```python
import os
from decouple import config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='your-fallback-secret-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    # Your apps
    'memos',
    'reservations',  # Add your apps here
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'your_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'your_project.wsgi.application'

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='reserveit_db'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default='mypassword123'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True
```

## Step 3: Running the Application

### 3.1 Start PostgreSQL Only (for development)

```bash
# Start only the database
docker-compose up db -d

# Check if it's running
docker-compose ps
```

### 3.2 Run Django Locally (connecting to Docker PostgreSQL)

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### 3.3 Run Everything with Docker

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

## Step 4: Useful Docker Commands

### 4.1 Basic Commands

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs

# View specific service logs
docker-compose logs web
docker-compose logs db
```

### 4.2 Database Management

```bash
# Connect to PostgreSQL container
docker-compose exec db psql -U postgres -d reserveit_db

# Run Django migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Django shell
docker-compose exec web python manage.py shell
```

### 4.3 Cleanup Commands

```bash
# Stop and remove containers
docker-compose down

# Remove containers and volumes
docker-compose down -v

# Remove everything including images
docker-compose down --rmi all -v
```

## Step 5: Testing the Setup

### 5.1 Check Database Connection

Create a simple test file `test_db.py`:

```python
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from django.db import connection

def test_database_connection():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"Database connection successful: {result}")
    except Exception as e:
        print(f"Database connection failed: {e}")

if __name__ == "__main__":
    test_database_connection()
```

Run: `python test_db.py`

### 5.2 Create Sample Models

In your `memos/models.py`:

```python
from django.db import models
from django.contrib.auth.models import User

class Memo(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Reservation(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.start_time}"
```

## Step 6: Common Issues and Solutions

### 6.1 Database Connection Errors

**Problem**: `connection to server at "localhost" (127.0.0.1), port 5432 failed`

**Solution**:
```bash
# Check if PostgreSQL container is running
docker-compose ps

# Restart the database
docker-compose restart db
```

### 6.2 Migration Issues

**Problem**: `relation "django_migrations" does not exist`

**Solution**:
```bash
# Reset migrations
docker-compose exec web python manage.py migrate --run-syncdb
```

### 6.3 Permission Errors

**Problem**: Permission denied errors in Docker

**Solution**:
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

## Step 7: Production Tips

### 7.1 Environment Variables

Use separate `.env` files for different environments:
- `.env.development`
- `.env.production`

### 7.2 Database Backups

```bash
# Create backup
docker-compose exec db pg_dump -U postgres reserveit_db > backup.sql

# Restore backup
docker-compose exec -T db psql -U postgres reserveit_db < backup.sql
```

### 7.3 Security Considerations

- Use strong passwords
- Don't commit `.env` files
- Use environment-specific settings
- Enable SSL in production

## Next Steps

1. **Add your Django apps** (memos, reservations)
2. **Create API endpoints** with Django REST Framework
3. **Connect with React frontend**
4. **Add authentication** and user management
5. **Implement reservation logic**
6. **Add tests** for your applications

This setup gives you a solid foundation for developing your ReserveIt app with PostgreSQL and Django using Docker!