# ReserveIt App

A reservation calendar application with memo creation functionality. Built with Django backend, PostgreSQL database, and React Next.js frontend.

## Features

- **Reservation Calendar**: Create and manage calendar events
- **Personal Memos**: Create and organize your own memos
- **Full-Stack Architecture**: Modern web application with REST API

## Tech Stack

- **Backend**: Python Django
- **Database**: PostgreSQL
- **Frontend**: React with Next.js
- **Development Environment**: Windows WSL (Windows Subsystem for Linux)

## Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL
- Windows WSL (if developing on Windows)

## Installation

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone git@github.com:ayekyiphyu/api_create.git
   cd api_create
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows WSL
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   ```bash
   # Install PostgreSQL (Ubuntu/WSL)
   sudo apt update
   sudo apt install postgresql postgresql-contrib

   # Start PostgreSQL service
   sudo service postgresql start

   # Create database
   sudo -u postgres createdb reserveit_db
   ```

5. **Environment Configuration**
   ```bash
   # Copy environment file
   cp .env.example .env

   # Edit .env file with your database credentials
   nano .env
   ```

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Start development server**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend  # or wherever your Next.js app is located
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

## Usage

1. **Access the application**
   - Backend API: `http://localhost:8000`
   - Frontend: `http://localhost:3000`
   - Admin Panel: `http://localhost:8000/admin`

2. **Create reservations**
   - Navigate to the calendar interface
   - Click on desired date/time slots
   - Fill in reservation details

3. **Manage memos**
   - Access memo section
   - Create, edit, and organize personal notes

## Development

### Running Tests
```bash
# Backend tests
python manage.py test

# Frontend tests
npm test
```

### Code Style
```bash
# Python formatting
black .
flake8 .

# JavaScript formatting
npm run lint
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -m 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- **Author**: AYE KYI PHYU
- **Email**: shinchan.lilo92@gmail.com
- **GitHub**: [@ayekyiphyu](https://github.com/ayekyiphyu)

## Troubleshooting

### Common Issues

- **PostgreSQL connection errors**: Ensure PostgreSQL service is running
- **Permission denied**: Use `sudo` for system-level operations in WSL
- **Port conflicts**: Check if ports 3000 and 8000 are available

### WSL-Specific Notes

- PostgreSQL service may need to be started manually: `sudo service postgresql start`
- File permissions might need adjustment when working between Windows and WSL



### Password

``` bash
## superuser

 * username : test@gmail.com
 * password : test12345

# normaluser
* username : mt@gmail.com
* password : test12345

```