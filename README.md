# extrackr - Personal Finance Tracker

A comprehensive Django web application for personal finance management with dual-view interface (desktop/mobile), user authentication, and advanced reporting capabilities.

## Features

### Core Features ✅
- **Income and Expense Tracking**: Complete CRUD operations for financial transactions
- **User Authentication**: Registration, login, logout, and password reset functionality
- **Category Management**: Predefined categories for income and expenses
- **Dual-View Interface**: Optimized desktop and mobile layouts
- **Dashboard Analytics**: Real-time financial overview with charts and statistics

### Advanced Features ✅
- **Budget Management**: Set and track monthly/quarterly/yearly budgets
- **Recurring Transactions**: Automate recurring income and expenses
- **Data Visualization**: Interactive charts using Plotly.js
- **Report Generation**: 
  - PDF reports (WeasyPrint)
  - Excel exports (openpyxl)
- **Responsive Design**: Mobile-first approach with Tailwind CSS

### Technical Features ✅
- **Django 4.2.7**: Modern Django framework
- **PostgreSQL Support**: Production-ready database configuration
- **Docker Support**: Containerized deployment ready
- **Admin Interface**: Comprehensive Django admin panel
- **Security**: CSRF protection, secure password handling

## Project Structure

```
extrackr/
├── extrackr_project/          # Django project settings
├── accounts/                  # User authentication app
├── transactions/              # Core financial transactions app
├── reports/                   # Reporting and analytics app
├── templates/                 # HTML templates
│   ├── base/                 # Base templates
│   ├── accounts/             # Account-related templates
│   ├── transactions/         # Transaction templates
│   └── reports/              # Report templates
├── static/                   # Static files (CSS, JS, images)
├── media/                    # User-uploaded files
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
└── PLAN.md                  # Development roadmap
```

## Installation & Setup

### Prerequisites
- Python 3.11+
- PostgreSQL (optional, SQLite for development)
- Docker (optional)

### Local Development

1. **Clone the repository**
```bash
git clone <repository-url>
cd extrackr
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment setup**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Database setup**
```bash
python manage.py migrate
python manage.py create_sample_data
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run development server**
```bash
python manage.py runserver
```

### Docker Setup

1. **Build and run with Docker Compose**
```bash
docker-compose up --build
```

2. **Access the application**
- Web app: http://localhost:8000
- Admin panel: http://localhost:8000/admin

## Default Credentials

### Admin User
- **Username**: admin
- **Password**: admin123
- **Email**: admin@extrackr.com

### Demo User
- **Username**: demo
- **Password**: demo123
- **Email**: demo@extrackr.com

## Usage

### Dashboard
- View financial overview with income/expense statistics
- Interactive charts showing monthly trends and category breakdowns
- Quick actions for adding transactions and setting budgets

### Transactions
- Add new income/expense entries with categories and descriptions
- Edit or delete existing transactions
- Filter by date range, category, or transaction type
- Search functionality for finding specific transactions

### Budgets
- Set monthly, quarterly, or yearly budgets for different categories
- Track budget usage with visual progress indicators
- Receive alerts when approaching budget limits

### Reports
- Generate PDF and Excel reports for any date range
- Customizable report types (summary, detailed, category-focused)
- Analytics dashboard with interactive charts and insights

### Recurring Transactions
- Set up automatic recurring income and expenses
- Choose from daily, weekly, monthly, quarterly, or yearly frequencies
- Automatic transaction creation based on schedule

## Technology Stack

### Backend
- **Django 4.2.7**: Web framework
- **PostgreSQL**: Production database (SQLite for development)
- **Django ORM**: Database abstraction
- **Python-decouple**: Environment variable management

### Frontend
- **Django Templates**: Server-side rendering
- **Tailwind CSS**: Utility-first CSS framework
- **Font Awesome**: Icon library
- **Plotly.js**: Interactive charts
- **Vanilla JavaScript**: Custom functionality

### Reports & Analytics
- **WeasyPrint**: PDF generation
- **OpenPyXL**: Excel file creation
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing

### Deployment
- **Docker**: Containerization
- **Gunicorn**: WSGI server
- **WhiteNoise**: Static file serving

## API Endpoints

### Transactions API
- `GET /transactions/api/stats/` - Get transaction statistics
- `GET /transactions/api/monthly-trend/` - Get monthly trend data
- `GET /transactions/api/category-breakdown/` - Get category breakdown

### Reports API
- `GET /reports/income-expense/` - Income vs expense chart data
- `GET /reports/category-analysis/` - Category analysis data
- `GET /reports/trends/` - Trend analysis data

## Security Features

- **CSRF Protection**: Cross-site request forgery protection
- **Secure Password Handling**: Django's built-in password hashing
- **User Authentication**: Session-based authentication
- **Environment Variables**: Sensitive data stored in environment
- **HTTPS Ready**: Production-ready security headers

## Deployment

### CloudPanel Deployment
The application is configured for easy deployment on CloudPanel:

1. Upload project files to your server
2. Configure environment variables
3. Set up PostgreSQL database
4. Run migrations and collect static files
5. Configure Gunicorn and Nginx

### Docker Deployment
Ready-to-use Docker configuration for any containerized environment:

```bash
docker build -t extrackr .
docker run -p 8000:8000 extrackr
```

## Development Roadmap

See [PLAN.md](PLAN.md) for detailed development checklist and future enhancements.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source. Feel free to use, modify, and distribute.

## Support

For issues, feature requests, or questions:
- Create an issue in the repository
- Check the documentation in PLAN.md
- Review the sample data for usage examples

---

Built with ❤️ for personal finance management