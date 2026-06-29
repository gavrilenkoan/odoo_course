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
- `demo/` – demo data
- `__manifest__.py` – module definition

### Requirements
- Odoo 19.0
- PostgreSQL
