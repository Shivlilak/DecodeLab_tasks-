
# Project 3 – SQL Data Analysis

## Internship
**DecodeLabs – Data Analytics Internship**  
**Batch 2026**

## Project Overview

This project focuses on **SQL Data Analysis** using a cleaned e-commerce orders dataset.

The objective is to use SQL queries to extract meaningful business insights by filtering, sorting, grouping, and aggregating the data.

## Dataset

The dataset contains e-commerce order information with the following fields:

- OrderID
- Date
- CustomerID
- Product
- Quantity
- UnitPrice
- ShippingAddress
- PaymentMethod
- OrderStatus
- TrackingNumber
- ItemsInCart
- CouponCode
- ReferralSource
- TotalPrice

## Objectives

- Extract data using SQL `SELECT` queries
- Filter records using `WHERE`
- Sort data using `ORDER BY`
- Group data using `GROUP BY`
- Perform calculations using aggregate functions
- Analyze products, payment methods, order statuses, and referral sources
- Use `HAVING` to filter grouped results
- Calculate percentage contribution to total sales
- Extract useful business insights from the dataset

## SQL Concepts Used

- SELECT
- WHERE
- ORDER BY
- GROUP BY
- HAVING
- COUNT()
- SUM()
- AVG()
- MIN()
- MAX()
- ROUND()
- Subqueries
- IN
- BETWEEN

## Analysis Performed

### 1. Basic Data Exploration
Used SQL queries to view records and calculate the total number of orders.

### 2. Data Filtering
Filtered orders based on:
- Order status
- Payment method
- Order value
- Date range
- Coupon usage

### 3. Product Analysis
Analyzed each product based on:
- Number of orders
- Total revenue
- Average order value
- Units sold

### 4. Payment Method Analysis
Compared different payment methods using:
- Order count
- Total revenue
- Average order value

### 5. Order Status Analysis
Analyzed orders based on their status such as:
- Delivered
- Shipped
- Pending
- Cancelled
- Returned

### 6. Quantity Analysis
Analyzed how order quantity affects:
- Number of orders
- Total revenue
- Average order value

### 7. Referral Source Analysis
Compared referral sources based on:
- Order count
- Revenue
- Average order value

### 8. Percentage Contribution
Calculated the percentage contribution of products, payment methods, and referral sources to total sales.

## Tools Used

- SQL
- SQLite
- Excel

## Files Included

- `Project_3_SQL_Analysis.sql` – SQL queries used for the analysis
- `Project_3_SQL_Results.xlsx` – Results and outputs of the SQL analysis

## Key Learning Outcomes

Through this project, I practiced:

- Writing SQL queries
- Filtering and sorting data
- Grouping and aggregating data
- Extracting business insights
- Using SQL for data analysis and decision support

## Conclusion

This project provided hands-on experience in using SQL to analyze an e-commerce dataset and extract meaningful business insights through filtering, grouping, aggregation, and percentage analysis.
