# Source Systems

---

## Project Information

| Property     | Value                                            |
|--------------|--------------------------------------------------|
| Project      | Enterprise Retail Sales Analytics Data Warehouse |
| Version      | 1.0                                              |
| Author       | Zam Walton P M                                   |
| Last Updated | July 2026                                        |

---

# Overview

The Enterprise Retail Sales Analytics Data Warehouse integrates data from multiple operational source systems across the retail business. Each system serves a different business function and provides data required for analytical reporting.

The ETL pipeline extracts data from these systems, validates it, transforms it into a common format, and loads it into the PostgreSQL Enterprise Data Warehouse.

---

# Source System Summary

| Source System  | Type        | Business Area        | Refresh Frequency | Primary Output       |
|----------------|-------------|----------------------|-------------------|----------------------|
| POS            | Transaction | Retail Stores        | Daily             | Store Sales          |
| Online Store   | Transaction | E-Commerce           | Daily             | Online Sales         |
| CRM            | Master      | Customer Management  | Daily             | Customer Data        |
| Product Master | Master      | Product Management   | Weekly            | Product Catalog      |
| Store Master   | Master      | Retail Operations    | Weekly            | Store Information    |
| HR             | Master      | Human Resources      | Weekly            | Employee Information |
| Promotions     | Master      | Marketing            | Daily             | Promotion Details    |
| Suppliers      | Master      | Procurement          | Monthly           | Supplier Information |
| Inventory      | Operational | Warehouse Operations | Daily             | Inventory Levels     |

---

# Source System Details

## 1. POS (Point of Sale)

### Business Purpose

Captures transactions from physical retail stores.

### Example Data

- Transaction ID
- Store ID
- Product ID
- Employee ID
- Customer ID
- Quantity
- Unit Price
- Discount
- Payment Method
- Transaction Timestamp

### Data Characteristics

| Property       | Value             |
|----------------|-------------------|
| Owner          | Retail Operations |
| Refresh        | Daily             |
| Estimated Rows | 250,000           |
| Primary Key    | transaction_id    |
| File           | sales_pos.csv     |

---

## 2. Online Store

### Business Purpose

Captures customer purchases made through the company's e-commerce platform.

### Example Data

- Order ID
- Customer ID
- Product ID
- Promotion ID
- Quantity
- Unit Price
- Shipping Method
- Delivery Status
- Order Timestamp

### Data Characteristics

| Property       | Value            |
|----------------|------------------|
| Owner          | E-Commerce Team  |
| Refresh        | Daily            |
| Estimated Rows | 150,000          |
| Primary Key    | order_id         |
| File           | sales_online.csv |

---

## 3. CRM

### Business Purpose

Stores customer master data used across the organization.

### Example Data

- Customer ID
- First Name
- Last Name
- Gender
- Date of Birth
- Email
- Phone
- City
- State
- Loyalty Tier
- Registration Date

### Data Characteristics

| Property       | Value               |
|----------------|---------------------|
| Owner          | Customer Experience |
| Refresh        | Daily               |
| Estimated Rows | 10,000              |
| Primary Key    | customer_id         |
| File           | customers.csv       |

---

## 4. Product Master

### Business Purpose

Maintains the organization's product catalog.

### Example Data

- Product ID
- Product Name
- Brand
- Category
- Subcategory
- Cost Price
- Selling Price
- Supplier ID

### Data Characteristics

| Property       | Value              |
|----------------|--------------------|
| Owner          | Product Management |
| Refresh        | Weekly             |
| Estimated Rows | 2,000              |
| Primary Key    | product_id         |
| File           | products.csv       |

---

## 5. Store Master

### Business Purpose

Stores information about physical retail locations.

### Example Data

- Store ID
- Store Name
- City
- State
- Region
- Opening Date
- Store Type

### Data Characteristics

| Property       | Value             |
|----------------|-------------------|
| Owner          | Retail Operations |
| Refresh        | Weekly            |
| Estimated Rows | 100               |
| Primary Key    | store_id          |
| File           | stores.csv        |

---

## 6. HR

### Business Purpose

Stores employee information.

### Example Data

- Employee ID
- Employee Name
- Department
- Job Title
- Hire Date
- Store ID
- Manager

### Data Characteristics

| Property       | Value           |
|----------------|-----------------|
| Owner          | Human Resources |
| Refresh        | Weekly          |
| Estimated Rows | 500             |
| Primary Key    | employee_id     |
| File           | employees.csv   |

---

## 7. Promotions

### Business Purpose

Stores marketing campaigns and promotional discounts.

### Example Data

- Promotion ID
- Promotion Name
- Discount Percentage
- Start Date
- End Date
- Promotion Type

### Data Characteristics

| Property       | Value          |
|----------------|----------------|
| Owner          | Marketing      |
| Refresh        | Daily          |
| Estimated Rows | 100            |
| Primary Key    | promotion_id   |
| File           | promotions.csv |

---

## 8. Suppliers

### Business Purpose

Stores supplier master information.

### Example Data

- Supplier ID
- Supplier Name
- Country
- Contact Person
- Email
- Product Category

### Data Characteristics

| Property       | Value         |
|----------------|---------------|
| Owner          | Procurement   |
| Refresh        | Monthly       |
| Estimated Rows | 300           |
| Primary Key    | supplier_id   |
| File           | suppliers.csv |

---

## 9. Inventory

### Business Purpose

Tracks stock availability across stores and warehouses.

### Example Data

- Product ID
- Store ID
- Current Stock
- Reserved Stock
- Reorder Level
- Last Updated

### Data Characteristics

| Property       | Value                |
|----------------|----------------------|
| Owner          | Warehouse Operations |
| Refresh        | Daily                |
| Estimated Rows | 10,000               |
| Primary Key    | inventory_id         |
| File           | inventory_levels.csv |

---

# Source Data Quality Expectations

All source systems are expected to meet the following minimum quality standards:

- Primary keys must be unique.
- Mandatory fields must not contain null values.
- Numeric values must be within valid business ranges.
- Dates must use ISO 8601 format.
- Foreign keys must reference valid master records.
- Duplicate transactional records are not permitted.

---

# Summary

These operational systems provide the source data for the Enterprise Retail Sales Analytics Data Warehouse. Together they represent the retail organization's transactional and master data, enabling integrated reporting and analytics.