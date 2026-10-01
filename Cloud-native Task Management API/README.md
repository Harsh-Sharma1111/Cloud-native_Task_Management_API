# Cloud-native Task Management API

A robust, cloud-ready backend REST API for managing Agile tasks and sprints. This project is built using Python, Flask, and SQLAlchemy, following enterprise best practices such as the Application Factory pattern, modular Blueprint routing, and environment-based configuration. 

It is designed to easily transition from a local development environment (using MySQL or SQLite) to a production cloud environment (e.g., AWS RDS).

---

## 🚀 Technology Stack
- **Framework**: Flask (Python 3.10+)
- **Database ORM**: SQLAlchemy 
- **Database Migrations**: Flask-Migrate (Alembic)
- **Serialization & Validation**: Marshmallow
- **Authentication**: PyJWT (JSON Web Tokens)
- **Cross-Origin Resource Sharing**: Flask-CORS
- **Local Database**: MySQL (`pymysql` driver) with SQLite available as an easy fallback
- **Cloud Database (Ready)**: AWS RDS configured with connection pooling and SSL

---

## 🏗️ Project Progress & Phase Breakdown

### ✅ Phase 0: Foundation & Application Setup
- **Directory Structure:** Set up a clean, scalable project structure (`backend/app/`, `backend/migrations/`, etc.).
- **App Factory Pattern:** Implemented the `create_app()` factory function to allow isolated testing and scalable configuration management.
- **Environment Configurations:** Configured dynamic environments (Dev, Test, Prod) through `config.py` and `.env`.
- **Global Error Handling:** Implemented centralized, consistent JSON responses for HTTP errors (400, 404, 500).

### ✅ Phase 1: Database Modeling (SQLAlchemy)
- **Schema Design:** Designed a relational database schema mirroring an Agile workflow.
- **Models Implemented (`app/models.py`)**:
  - **User**: Represents team members and admins (includes secure `werkzeug` password hashing).
  - **Sprint**: Time-boxed workflow cycles mapping to start/end dates and statuses (planned, active, completed).
  - **Task**: The core work item (todo, in_progress, done) supporting dynamic priorities and mapped to specific sprints and assignees via Foreign Keys.
- **Indexes:** Defined explicit composite indexes to optimize read queries when filtering tasks by assignee or sprint.

### ✅ Phase 2: RESTful API Endpoints (Blueprints)
- **Modular Routing:** Abstracted controllers into Flask Blueprints.
- **Marshmallow Schemas (`app/schemas/`):** Created robust serialization schemas to handle JSON data validation on incoming requests and formatting on outgoing responses.
- **CRUD Operations**: Complete CRUD routes built for:
  - `users.py`: Retrieve and manage team members.
  - `sprints.py`: Create sprints and track their lifecycles.
  - `tasks.py`: Full task management, including filtering endpoints by status, priority, and assignee.

### ✅ Phase 3: Authentication & API Testing
- **JWT Auth (`auth.py`)**: Implemented stateless JSON Web Token authentication.
- **Protected Routes**: Created a custom `@token_required` decorator to protect sensitive application routes from unauthorized access.
- **Testing**:
  - Exported a complete **Postman Collection** (`TaskManagementAPI.postman_collection.json`) containing configured requests and pre-request scripts for easy API exploration and automated token handling.

### ✅ Phase 4: Database Migrations & MySQL/Cloud Readiness
- **Database Migrations**: Integrated **Flask-Migrate** to programmatically track and manage schema changes over time.
- **Local MySQL Integration**: Switched the local primary database from SQLite to **MySQL** (`taskdb_dev`).
- **Database Seeding (`seed.py`)**: Created a standalone script to instantly populate the database with realistic mock data (creating an admin user, team members, active sprints, and 8 distributed tasks).
- **AWS RDS Cloud Configuration**: Hardened the `ProductionConfig` inside `config.py` for deployment:
  - Dynamically builds the DB connection URI from atomic environment variables (`DB_USER`, `DB_PASSWORD`, `DB_HOST`, etc.).
  - Enforced SSL connections natively (`require_secure_transport`).
  - Implemented SQL connection pooling optimizations (`pool_pre_ping=True`, `pool_recycle=280`) to actively prevent stale connections and "MySQL server has gone away" timeouts typical of AWS RDS.

### ✅ Phase 5: Frontend React SPA (Single Page Application)
- **Modern Scaffolding**: Initialized a blazing-fast React environment utilizing **Vite** and styled completely with the modern **Tailwind CSS v4** engine.
- **Axios API Client**: Built a dedicated API layer (`client.js`, `tasksApi.js`, etc.) utilizing Axios interceptors to automatically parse environment variables (`VITE_API_BASE_URL`) and securely attach JWTs to outgoing requests from `localStorage`.
- **Authentication & Security (`AuthContext`)**: 
  - Implemented a React Context API wrapper to globally manage the `user` and `token` state.
  - Built a `ProtectedRoute` component wrapping React Router to intercept unauthorized visits and redirect to a polished Login screen while preserving intended navigation state.
- **Interactive Kanban Board**: 
  - Utilized `@hello-pangea/dnd` to create a 3-column drag-and-drop Sprint board.
  - Engineered **Optimistic UI updates** for card dragging—instantly updating the frontend while silently handling `PUT` requests to the API, complete with gracefully rolling back the UI and firing `react-hot-toast` error notifications if the backend request fails.
- **Task Management Modal**: Created an overlay modal handling both Task Creation and Editing, auto-populating Sprint and Assignee dropdowns, and allowing Task Deletion (with confirmation).
- **Data Visualization**: Integrated **Recharts** to display a horizontal, color-coded, live-updating progress chart summarizing the currently selected Sprint's completion status.

### ✅ Phase 6: Automated Testing Quality Assurance
- **Backend (Pytest)**:
  - Engineered comprehensive integration tests covering all CRUD operations for Tasks.
  - Developed reusable pytest fixtures (`app`, `client`, `auth_headers`) utilizing an in-memory SQLite database mapped through a dedicated `TestingConfig` class to guarantee fast, completely isolated test runs without altering development data.
  - Achieved robust API route coverage with `pytest-cov`, strictly validating authentication requirements, bad payloads, and schema validation error strings.
- **Frontend (Vitest & React Testing Library)**:
  - Setup a full JS DOM testing environment configured via `setupTests.js` mocking browser-native APIs (like `window.matchMedia` for toasts).
  - Wrote integration tests for the `KanbanBoard` verifying critical states (Loading spinner display, successful task fetching/sorting into columns, and failure/error states gracefully rendering error banners).

---

## 🛠️ Comprehensive Local Development Setup

Follow these steps to get the API running locally on your machine.

### 1. Prerequisites
- Python 3.10+ installed.
- MySQL Server installed and running locally.

### 2. Environment Setup
First, navigate to the backend folder and create a virtual environment:
```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
Install all required packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the `backend/` directory. You can use `.env.example` as a template:
```ini
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_super_secret_key
JWT_SECRET_KEY=your_jwt_secret_key

# Database connection (Ensure you replace YOUR_PASSWORD with your actual local MySQL root password)
SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:YOUR_PASSWORD@localhost/taskdb_dev
```

### 5. Initialize the Database & Run Migrations
Log into your local MySQL instance and create the development database:
```bash
# Enter your MySQL shell
mysql -u root -p

# Inside the MySQL shell, run:
CREATE DATABASE taskdb_dev;
EXIT;
```
Now, use Flask-Migrate to create the tables in your new database:
```bash
flask db upgrade
```

### 6. Seed the Database with Mock Data
To avoid starting with an empty application, run the seeding script. This will wipe any existing data safely and insert 3 users, 2 sprints, and 8 tasks.
```bash
python seed.py
```
*Note: The `seed.py` script creates the following users, all with the password `password123`:*
- `admin@example.com` (Role: Admin)
- `alice@example.com` (Role: Member)
- `bob@example.com` (Role: Member)

### 7. Run the Development Server (Backend)
Start the Flask application:
```bash
python run.py
```
The API will be available at `http://localhost:5000/`.

### 8. Run the Frontend React Application
Open a **new terminal window**, navigate to the `frontend/` directory, install the Node dependencies, and start Vite:
```bash
cd frontend
npm install
npm run dev
```
The React application will be available at `http://localhost:5173/`.

---

## 🧪 Testing the Application

### 1. Automated Backend Tests (Pytest)
To run the automated backend test suite with full coverage reporting:
```bash
cd backend
python -m pytest --cov=app tests/
```
*Tests are isolated and utilize an in-memory SQLite database so they will not affect your local `taskdb_dev` data.*

### 2. Automated Frontend Tests (Vitest)
To run the React component tests:
```bash
cd frontend
npm run test
```

### 3. Manual API Exploration (Postman)
To manually test and explore the API, import the provided `TaskManagementAPI.postman_collection.json` file into **Postman**. 
1. Use the `/api/auth/login` endpoint with `admin@example.com` and `password123` to receive a JWT.
2. The collection is configured to save the JWT to an environment variable, allowing you to instantly hit protected routes like `GET /api/tasks` or `POST /api/sprints`.
