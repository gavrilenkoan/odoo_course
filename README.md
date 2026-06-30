# Odoo Learning Modules

## 2. Create Module

A simple Odoo module created as part of the `02-create-module` lesson.

Implements a basic library system with books, authors, and demo data.

### Features
- Book management (`library.book`)
- Author relation using `res.partner`
- Menu structure
- Form and list views
- Demo data

### Structure
- `models/` – Python models
- `views/` – XML views and menus
- `security/` – access rights
- `static/` – resources
- `demo/` – demo data
- `__manifest__.py` – module definition

## 2. HR Hospital (Homework)

A simple Odoo module created as homework for the `02-create-module` lesson.

Implements a basic hospital management system with doctors, patients, diseases, and visits.

### Features
- Doctor management (`hospital.doctor`)
- Patient management (`hospital.patient`)
- Disease dictionary (`hospital.disease`)
- Visit tracking (`hospital.visit`)
- Menu structure (Hospital → Doctors / Patients / Diseases / Visits)
- Form and list views for all models
- Access rights for internal users (`base.group_user`)
- Master and demo data

### Structure
- `models/` – Python models (Doctor, Patient, Disease, Visit)
- `views/` – XML views, actions, and menus
- `security/` – access rights (ir.model.access.csv)
- `static/` – resources
- `data/` – master data (diseases)
- `demo/` – demo data (doctors, patients)
- `__manifest__.py` – module definition