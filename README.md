# Group1_HIT237

## 👥 Members
- Pralin Dhungana  
- Umme Habiba  
- Gaurab Gaihre  
- Carlos Cordoba  

---

## Overview of Project

This repository documents the design and development of a Django-based web application addressing the **Remote Housing Crisis in the Northern Territory (NT)**.

The system provides a structured platform for managing repair requests and maintenance processes to improve housing efficiency and availability in remote communities.

---

##  Problem Context

The Northern Territory faces significant housing challenges, including:

- Approximately **6,000 people on the waiting list** for public housing  
- Delays in repair and maintenance processes  
- Inefficiencies in housing turnover  
- Poor maintenance reducing housing availability  

This application helps address these issues through structured repair request tracking and maintenance management.

---

##  Objective

The application aims to:

- Enable tenants to **report and track repair requests**  
- Improve communication between tenants, contractors, and housing authorities  
- Ensure effective maintenance of housing assets  
- Reduce downtime and improve housing availability  

---

##  Target Audience

- Tenants  
- Maintenance staff / contractors  
- Housing authority personnel  

---

## ⚙️ Features

- Submit repair requests  
- Track request status (pending, in progress, completed)  
- View repair history of dwellings  
- Categorize issues (plumbing, electrical, structural)  
- Monitor maintenance activity across communities  

---

## Technology Stack

- **Framework:** Django  
- **Language:** Python  
- **Database:** SQLite (development environment)  
- **Version Control:** GitHub  

---

##  Development Strategy

This project follows an **architecture-driven approach**:

- Architectural decisions documented using **ADR (Architecture Decision Record)**  
- Object-oriented design principles (encapsulation, modularity)  
- Django best practices:
  - DRY (Don't Repeat Yourself)  
  - Fat models, thin views  
- Use of:
  - Class-Based Views (CBVs)  
  - Optimized QuerySets (`select_related`)  
- AI-assisted tools used responsibly and reviewed by team  

---

#  Setup Instructions (MANDATORY FOR TESTING)

```bash
# Clone repository
git clone https://github.com/ccordoba24/Group1_HIT237.git

# Navigate into project
cd Group1_HIT237/proj_1

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r ..\requirements.txt

# Apply migrations
python manage.py migrate

# Load demo data (IMPORTANT STEP)
python manage.py seed_data

# Run server
python manage.py runserver

🔐 Demo Login Credentials

Run python manage.py seed_data before using these.

Admin (Full Access)
Username: adminfinal
Password: Admin12345
Test User (Tenant Simulation)
Username: testuser
Password: pralin206407