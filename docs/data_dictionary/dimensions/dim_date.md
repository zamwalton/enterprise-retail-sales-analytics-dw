# Date Dimension

## Purpose

Stores calendar information for analytical reporting.

Unlike other dimensions, this table is generated programmatically and is not sourced from operational systems.

---

## Primary Key

date_key

---

## Columns

| Column         | Description                    |
|----------------|--------------------------------|
| date_key       | Integer key in YYYYMMDD format |
| full_date      | Calendar date                  |
| day            | Day of month                   |
| day_name       | Name of the day                |
| week_of_year   | ISO week number                |
| month          | Month number                   |
| month_name     | Month name                     |
| quarter        | Quarter number                 |
| year           | Calendar year                  |
| is_weekend     | Weekend indicator              |
| is_month_end   | Month-end indicator            |
| is_quarter_end | Quarter-end indicator          |
| is_year_end    | Year-end indicator             |

---

## Business Rules

- One record per calendar date.
- Date Key format: YYYYMMDD.
- Generated programmatically.
- No duplicate dates.