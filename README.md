# 🏥 SmartHospital - Django Hospital Management System

A comprehensive hospital management system built with Django and Django REST Framework that handles appointments, patient records, doctor management, and more with a modern API-first approach.

![Django](https://img.shields.io/badge/Django-5.2.7-green)
![DRF](https://img.shields.io/badge/Django_REST_Framework-3.15-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

## ✨ Features

### 🎯 Core Functionality
- **Patient Management** - Complete patient profiles and records
- **Doctor Management** - Doctor profiles with specialization and availability
- **Appointment System** - Online/offline appointments with status tracking
- **Review & Rating** - Patient feedback with star ratings
- **Contact System** - Built-in contact form for inquiries

### 🛡️ Security & Moderation
- **Bad Word Filtering** - Automatic profanity filter for usernames and content
- **Email Verification** - SMTP-based account confirmation
- **CSRF Protection** - Secure form handling
- **Token Authentication** - REST API security

### 🚀 Technical Features
- **RESTful API** - Complete API with DRF
- **Docker Support** - Easy deployment with Docker Compose
- **Admin Interface** - Django admin for management
- **Media Handling** - Image uploads for profiles
- **Filtering & Search** - Advanced query capabilities

## 🏗️ Project Structure

```
SmartHospital/
├── Api/                    # REST API endpoints
├── appointment/           # Appointment management
├── contact_us/           # Contact form handling
├── doctor/               # Doctor profiles & management
├── patient/              # Patient profiles & records
├── service/              # Hospital services
├── SmartHospital/        # Project settings
├── docker-compose.yml    # Docker configuration
├── Dockerfile           # Container setup
└── requirements.txt     # Python dependencies
```

## 📋 Prerequisites

- Python 3.8+
- Docker & Docker Compose (optional)
- Gmail account for email services

## 🚀 Installation

### Method 1: Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/SheikhIshere/CliniZ-api-drf.git
   cd SmartHospital
   ```

2. **Create environment file**
   ```bash
   # Create .env file in project root
   echo "SECRET_KEY=your-secret-key-here" >> .env
   echo "email=your-email@gmail.com" >> .env
   echo "email_password=your-app-password" >> .env
   ```

3. **Start with Docker Compose**
   ```bash
   docker-compose up --build
   # Or run in detached mode
   docker-compose up -d
   ```

### Method 2: Manual Setup

1. **Create virtual environment**
   ```bash
   python -m venv linux_venv
   source linux_venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run development server**
   ```bash
   python manage.py runserver
   ```

## ⚙️ Environment Configuration

Create a `.env` file in the project root:

```env
SECRET_KEY=your-django-secret-key
email=your-gmail@gmail.com
email_password=your-google-app-password
```

**Note:** For Gmail, you need to use an [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password.

## 🎮 Usage

### Access Points

- **Admin Panel**: `http://localhost:8000/admin/`
- **API Root**: `http://localhost:8000/api/`
- **API Documentation**: `http://localhost:8000/api/schema/`

### Key API Endpoints

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/api/doctors/` | GET | List all doctors |
| `/api/patients/` | GET | List all patients |
| `/api/appointments/` | GET/POST | Manage appointments |
| `/api/reviews/` | GET/POST | Handle patient reviews |
| `/api/contact/` | POST | Submit contact forms |

## 🛡️ Bad Word Filtering

The system includes comprehensive profanity filtering:

- Automatic detection of inappropriate words in usernames and content
- Prevents abuse and maintains professional environment
- Customizable word list in `bad_words.py`

## 🐳 Docker Commands

```bash
# Start services
docker-compose up

# Stop services
docker-compose down

# View logs
docker-compose logs

# Rebuild images
docker-compose up --build
```

## 🔧 Management Commands

```bash
# Create superuser
docker-compose exec web python manage.py createsuperuser

# Run migrations
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic
```

## 📧 Email Configuration

The system uses Gmail SMTP for:
- User account verification
- Appointment notifications
- Contact form submissions
- Password reset functionality

## 🔐 Security Features

- CSRF protection
- Token-based authentication
- Secure file uploads
- Input validation and sanitization
- Bad word filtering system

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues:

1. Check the Docker logs: `docker-compose logs web`
2. Verify environment variables in `.env` file
3. Ensure all migrations are applied
4. Check email configuration for Gmail App Password

---

**Developed with ❤️ using Django & Docker**
