# Spy Cat Agency API

The **Spy Cat Agency API** is a RESTful application designed to streamline the operations of the Spy Cat Agency. This system allows the agency to manage their spy cats, assign them to missions, and track their progress as they spy on targets. 

The API provides functionality to manage spy cats, missions, and targets, ensuring that the process is both secure and efficient. Documentation for the API is available at the `/api/v1/swagger/` endpoint.

---

## Features

### Spy Cats
- Create a new spy cat with details like name, breed, years of experience, and salary.
- Update the salary of existing spy cats.
- Remove spy cats from the system.
- Retrieve a list of all spy cats or the details of a specific one.

### Missions and Targets
- Create a mission with associated targets in a single request.
- Update mission details, including marking targets as complete or adding notes (if allowed).
- Assign available spy cats to missions.
- List all missions or retrieve details for a specific one.
- Prevent deletion of missions already assigned to cats.

### General
- Validate cat breeds using the [TheCatAPI](https://api.thecatapi.com/v1/breeds).
- Ensure data integrity with appropriate validations and status codes.

---

## Technology Stack

- **Framework**: Django REST Framework
- **Database**: SQLite (lightweight and easy-to-use for testing)
- **API Documentation**: Available at `/api/v1/swagger/`

---

## Getting Started

Follow these steps to set up and run the project locally:

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/spy-cat-agency.git
cd spy-cat-agency
```
### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Apply Migrations
```bash
python manage.py migrate
```
### 5. Start the Development Server
```bash
python manage.py runserver
```
### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows
```