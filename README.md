# SmartMed

SmartMed is a medicine disposal and tracking platform designed to help users safely manage expired or unwanted medicines.

The project combines a FastAPI backend, PostgreSQL database, machine-learning components, and a frontend application.

## Project Structure

```text
SmartMed/
├── backend/          # FastAPI backend and REST APIs
├── frontend/         # Frontend application
├── ml/               # Machine-learning and medicine intelligence
├── database/         # Database-related files
├── dataset/          # Project datasets
├── README.md
└── .gitignore

Main Features

User registration and authentication
Admin authentication
JWT-based authorization
Medicine search
Medicine information lookup
Medicine disposal requests
Disposal tracking
Tracking status updates
Role-based access control
Machine-learning based medicine classification
Medicine disposal guidance
Frontend interface for interacting with the system.

Backend
The backend is built using:
Python
FastAPI
PostgreSQL
JWT authentication
SQL-based database operations
The backend provides APIs for users, administrators, medicines, disposal requests, and tracking.
Running the Backend

From the project root:

cd backend
..\venv\Scripts\python.exe -m uvicorn main:app --reload

The API documentation is available through FastAPI Swagger UI:

http://127.0.0.1:8000/docs
Frontend

The frontend is located in the frontend/ directory.

It provides the user interface for interacting with SmartMed and communicating with the backend APIs.

Machine Learning

The machine-learning components are located in the ml/ directory.

The ML module contains:

Dataset analysis
Data preprocessing
Model training
Medicine classification
Prediction
Disposal intelligence
Backend integration
Model evaluation

Important ML files include:

ml/
├── analysis/
├── disposal/
├── integration/
├── model/
├── prediction/
└── preprocessing/
Authentication

SmartMed uses JWT-based authentication.

There are two main roles:

User
Admin

Protected API endpoints require a valid JWT access token.

Role-based authorization prevents users from accessing administrator-only endpoints and prevents administrators from accessing user-only endpoints where applicable.

Database

SmartMed uses PostgreSQL for persistent data storage.

The database contains information related to:

Users
Administrators
Medicines
Disposal requests
Tracking information
Medicine manufacturers and related data

Database credentials and other secrets must be stored in a local .env file and must not be committed to Git.

Security

The project uses:

JWT authentication
Password hashing
Role-based authorization
Environment variables for secrets
Protected API endpoints

The .env file is excluded from Git using .gitignore.

Team Development

The project is maintained collaboratively using Git and GitHub.

The repository uses:

main

as the primary branch.

For new development, contributors should preferably create a feature branch and submit a Pull Request for review before merging into main.

Example:

git checkout -b feature-name

After making changes:

git add .
git commit -m "Describe the change"
git push origin feature-name

Then create a Pull Request on GitHub.

Important

Do not commit:
.env files
Passwords
JWT secrets
Database credentials
Virtual environments
Other sensitive credentials

These files and values should remain local.

Project Goal

SmartMed aims to provide a centralized platform for identifying medicines, providing appropriate disposal guidance, submitting disposal requests, and tracking the disposal process.

The combination of the backend, frontend, database, and machine-learning components provides the foundation for a complete medicine-management and disposal solution.