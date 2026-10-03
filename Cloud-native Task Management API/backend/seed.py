import os
import sys
from datetime import date, timedelta
from werkzeug.security import generate_password_hash

# Ensure we can import from backend modules when run from project root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Sprint, Task
from config import config_by_name

def seed_db():
    # Use environment to determine config or default to 'dev'
    env = os.environ.get('FLASK_ENV', 'dev')
    config_class = config_by_name.get(env, config_by_name['dev'])
    app = create_app(config_class)
    
    with app.app_context():
        print("Creating tables if they don't exist...")
        db.create_all()
        
        print("Clearing existing data...")
        # Delete in reverse dependency order
        Task.query.delete()
        Sprint.query.delete()
        User.query.delete()
        
        print("Creating users...")
        admin = User(
            name="Admin User",
            email="admin@example.com",
            password_hash=generate_password_hash("password123"),
            role="admin"
        )
        member1 = User(
            name="Alice Developer",
            email="alice@example.com",
            password_hash=generate_password_hash("password123"),
            role="member"
        )
        member2 = User(
            name="Bob Designer",
            email="bob@example.com",
            password_hash=generate_password_hash("password123"),
            role="member"
        )
        
        db.session.add_all([admin, member1, member2])
        db.session.commit()
        
        print("Creating sprints...")
        today = date.today()
        active_sprint = Sprint(
            name="Sprint 1 - Foundation",
            start_date=today - timedelta(days=2),
            end_date=today + timedelta(days=12),
            status="active"
        )
        planned_sprint = Sprint(
            name="Sprint 2 - Core Features",
            start_date=today + timedelta(days=14),
            end_date=today + timedelta(days=28),
            status="planned"
        )
        
        db.session.add_all([active_sprint, planned_sprint])
        db.session.commit()
        
        print("Creating tasks...")
        tasks = [
            Task(
                title="Setup project repository",
                description="Initialize git and basic folder structure.",
                status="done",
                priority="high",
                sprint_id=active_sprint.id,
                assignee_id=admin.id
            ),
            Task(
                title="Design Database Schema",
                description="Create ERD and initial SQL scripts for models.",
                status="done",
                priority="high",
                sprint_id=active_sprint.id,
                assignee_id=member1.id
            ),
            Task(
                title="Implement Auth API",
                description="Create login and registration endpoints with JWT.",
                status="in_progress",
                priority="high",
                sprint_id=active_sprint.id,
                assignee_id=member1.id
            ),
            Task(
                title="Create UI Mockups",
                description="Design wireframes for the task dashboard.",
                status="in_progress",
                priority="medium",
                sprint_id=active_sprint.id,
                assignee_id=member2.id
            ),
            Task(
                title="Setup CI/CD pipeline",
                description="Configure GitHub Actions for automated testing.",
                status="todo",
                priority="medium",
                sprint_id=active_sprint.id,
                assignee_id=admin.id
            ),
            Task(
                title="Write Unit Tests for Models",
                description="Ensure test coverage for User, Sprint, and Task models.",
                status="todo",
                priority="medium",
                sprint_id=active_sprint.id,
                assignee_id=member1.id
            ),
            Task(
                title="Implement Task Filtering",
                description="Add query parameters to filter tasks by status and priority.",
                status="todo",
                priority="low",
                sprint_id=planned_sprint.id,
                assignee_id=member1.id
            ),
            Task(
                title="Design Landing Page",
                description="Create a beautiful marketing page for the app.",
                status="todo",
                priority="medium",
                sprint_id=planned_sprint.id,
                assignee_id=member2.id
            ),
        ]
        
        db.session.add_all(tasks)
        db.session.commit()
        
        print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed_db()
