# Coffee Shop Web Application

A modern web application for a coffee shop that allows users to sign up, sign in, view the coffee of the day, check promotions, track their loyalty points, and place orders.

## Features

- User authentication (sign up and login)
- Coffee of the day display
- Current promotions section
- Loyalty points tracking
- Menu with ordering functionality
- Responsive design for all devices

## Technologies Used

- Python 3.x
- Flask (Web Framework)
- SQLAlchemy (Database ORM)
- Bootstrap 5 (Frontend Framework)
- SQLite (Database)

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd coffee-shop
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

5. Run the application:
```bash
python app.py
```

6. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
coffee_shop/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── static/            # Static files (CSS, JS, images)
│   ├── css/
│   └── js/
├── templates/         # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   └── signup.html
└── README.md          # Project documentation
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 