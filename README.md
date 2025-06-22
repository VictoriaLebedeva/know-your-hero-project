# Web Application Security Practice

A simple web application for practicing secure authentication, authorization, and review management using Flask (backend) and a modern frontend (see `frontend/`).

## Features

- User registration and login with JWT-based authentication
- Secure cookie handling (HTTP-only, SameSite)
- Role-based access (basic)
- Add and view reviews for users
- RESTful API endpoints
- Input validation and error handling
- CORS enabled for frontend-backend communication

## Project Structure

```
web-application-security-practice/
├── backend/
│   ├── app.py                # Flask app entry point
│   ├── models.py             # SQLAlchemy models and DB setup
│   ├── requirements.txt      # Python dependencies
│   ├── auth/
│   │   └── auth.py           # Authentication routes
│   └── reviews/
│       └── reviews.py        # Review management routes
├── frontend/                 # Frontend (see its own README or package.json)
├── docker-compose.yaml       # For running backend/frontend with Docker
└── README.md                 # This file
```

## Setup & Usage

### Prerequisites
- Python 3.9+
- Node.js (for frontend)
- Docker (optional, for containerized setup)

### Backend Setup
1. Navigate to the `backend/` directory:
   ```sh
   cd backend
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set environment variables (e.g. in `.env` or your shell):
   - `SECRET_KEY` (required for JWT)
4. Run the backend:
   ```sh
   python app.py
   ```

### Frontend Setup
1. Navigate to the `frontend/` directory:
   ```sh
   cd frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Run the frontend:
   ```sh
   npm run dev
   ```

### Docker Compose (optional)
To run both backend and frontend with Docker:
```sh
docker-compose up --build
```

## API Endpoints (TBD Можно сделать сваггер)

### Authentication
- `POST /api/auth/register` — Register a new user
- `POST /api/auth/login` — Login and receive JWT in cookie
- `POST /api/auth/logout` — Logout (clears cookie)
- `GET /api/me` — Get current user info (requires authentication)

### Users
- `GET /api/users` — List all users (requires authentication)

### Reviews
- `GET /api/reviews` — List all reviews (requires authentication)
- `POST /api/reviews` — Create a new review (requires authentication)

## Assumptions

- Users must enter their real name as username during registration (in a real app, this would sync with an employee list).

## Security Notes
- JWT tokens are stored in HTTP-only cookies for security.
- CORS is restricted to the frontend origin.
- Input validation and error handling are implemented on the backend.
- Passwords are hashed before storage.

## License

This project is for educational and practice purposes only.