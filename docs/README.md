
Health Club Management System

Final Project COMP 3005
Author: Abdulrahman Al-Dousari

Overview

This project is a Health Club database system built using:

postgreSQL
SQLAlchemy ORM (Python)
pgAdmin
VS Code

The application manages members, trainers, rooms, class sessions, personal training sessions, invoices, and health metrics.
All tables, relationships, and data are created programmatically using SQLAlchemy.
No manual .sql files were used.

Project Structure

app/
    init_db.py
    seed_data.py
    main.py
    create_view.py
    create_trigger.py
    create_index.py

models/
    base.py
    entities.py
    __init__.py

docs/
    ERD.pdf
    README.md

config.py

.gitignore

How to Run the Project !!

Step 1: Install dependencies

Make sure you are inside the project folder:

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt


If there is no requirements.txt, install manually:

pip install sqlalchemy psycopg2

Step 2: Update your database connection

Open the file:

config.py


Then set your PostgreSQL username, password, and database name.

Step 3: Create all tables

python -m app.init_db

Step 4: Insert sample data

python -m app.seed_data

Step 5: Create the view, trigger, and index

python -m app.create_view

python -m app.create_trigger

python -m app.create_index

Step 6: Run the application
python -m app.main


The terminal menu will appear and you can test all features.

Screenshots

All required screenshots are included inside docs/ERD.pdf, including:

Tables in pgAdmin

View

Trigger and trigger function

Python application running

Video Demonstration



