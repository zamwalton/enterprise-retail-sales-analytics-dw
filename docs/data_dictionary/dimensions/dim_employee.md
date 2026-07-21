# Employee Dimension

## Purpose

Stores employee information for analytical reporting.

Implements Slowly Changing Dimension (SCD Type 2) to preserve historical changes to employee attributes.

---

## Primary Key

employee_key

---

## Business Key

employee_id

---

## Columns

| Column               | Description                     |
|----------------------|---------------------------------|
| employee_key         | Warehouse surrogate primary key |
| employee_id          | Business employee identifier    |
| employee_name        | Employee full name              |
| department           | Department name                 |
| job_title            | Employee designation            |
| manager_id           | Manager business identifier     |
| hire_date            | Employee hire date              |
| employment_status    | Active, On Leave, Terminated    |
| effective_start_date | Record effective start date     |
| effective_end_date   | Record effective end date       |
| is_current           | Current record indicator        |
| created_date         | ETL creation timestamp          |
| updated_date         | ETL update timestamp            |

---

## Business Rules

- Employee ID is required.
- Employee Name is required.
- Employment Status must be one of:
  - Active
  - On Leave
  - Terminated
- Implements SCD Type 2.