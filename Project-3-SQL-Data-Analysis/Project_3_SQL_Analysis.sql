/* =================================================================================
   PROJECT 3 - SQL DATA ANALYSIS
   DecodeLabs Data Analytics Internship | Batch 2026
   -----------------------------------------------------------------------------
   Objective: Use SQL queries to extract meaningful business insights from the
   cleaned e-commerce orders dataset (output of Project 1 / Project 2).

   Table used throughout this script: orders
   Columns: OrderID, Date, CustomerID, Product, Quantity, UnitPrice,
            ShippingAddress, PaymentMethod, OrderStatus, TrackingNumber,
            ItemsInCart, CouponCode, ReferralSource, TotalPrice

   Written in standard ANSI SQL (tested on SQLite; also runs on MySQL / PostgreSQL
   with minor syntax notes called out where relevant).
   ================================================================================= */


/* ---------------------------------------------------------------------------------
   0. CREATE TABLE (reference schema)
   ---------------------------------------------------------------------------------
   Not required to re-run if the table already exists (e.g. imported from
   cleaned_dataset.xlsx / cleaned_dataset.csv) — included here so the script is
   fully self-contained and reproducible from scratch.
   --------------------------------------------------------------------------------- */
CREATE TABLE IF NOT EXISTS orders (
    OrderID          TEXT,
    Date             DATE,
    CustomerID       TEXT,
    Product          TEXT,
    Quantity         INTEGER,
    UnitPrice        DECIMAL(10,2),
    ShippingAddress  TEXT,
    PaymentMethod    TEXT,
    OrderStatus      TEXT,
    TrackingNumber   TEXT,
    ItemsInCart      INTEGER,
    CouponCode       TEXT,
    ReferralSource   TEXT,
    TotalPrice       DECIMAL(10,2)
);


/* =================================================================================
   1. BASIC SELECT QUERIES - viewing the data
   ================================================================================= */

-- 1.1 View every column for the first 10 orders (a quick look at the raw data)
SELECT *
FROM orders
LIMIT 10;

-- 1.2 Count how many rows (orders) are in the table
SELECT COUNT(*) AS TotalOrders
FROM orders;


/* =================================================================================
   2. SELECTING SPECIFIC COLUMNS
   ================================================================================= */

-- 2.1 Pull only the columns needed for a simple order summary
SELECT OrderID, Date, Product, Quantity, TotalPrice
FROM orders
LIMIT 10;

-- 2.2 Rename columns in the output using aliases (AS) for a friendlier report
SELECT OrderID       AS Order_Number,
       Product       AS Item_Purchased,
       TotalPrice    AS Order_Value
FROM orders
LIMIT 10;


/* =================================================================================
   3. WHERE QUERIES - filtering records
   ================================================================================= */

-- 3.1 Orders that were successfully Delivered
SELECT OrderID, Product, TotalPrice, OrderStatus
FROM orders
WHERE OrderStatus = 'Delivered';

-- 3.2 High-value Delivered orders (multiple conditions combined with AND)
SELECT OrderID, Product, TotalPrice, OrderStatus
FROM orders
WHERE OrderStatus = 'Delivered'
  AND TotalPrice > 2000;

-- 3.3 Orders paid by either Credit Card or Online (IN operator)
SELECT OrderID, PaymentMethod, TotalPrice
FROM orders
WHERE PaymentMethod IN ('Credit Card', 'Online');

-- 3.4 Orders placed without any coupon (checking for NULL / blank values)
SELECT OrderID, Product, TotalPrice, CouponCode
FROM orders
WHERE CouponCode IS NULL;

-- 3.5 Orders within a specific date range (BETWEEN operator)
SELECT OrderID, Date, Product, TotalPrice
FROM orders
WHERE Date BETWEEN '2024-01-01' AND '2024-01-31';


/* =================================================================================
   4. ORDER BY - sorting results
   ================================================================================= */

-- 4.1 Top 10 highest-value orders (descending sort)
SELECT OrderID, Product, TotalPrice
FROM orders
ORDER BY TotalPrice DESC
LIMIT 10;

-- 4.2 Orders sorted from oldest to newest (ascending sort)
SELECT OrderID, Date, TotalPrice
FROM orders
ORDER BY Date ASC
LIMIT 10;

-- 4.3 Sort by multiple columns: Product (A-Z), then TotalPrice (highest first)
SELECT Product, OrderID, TotalPrice
FROM orders
ORDER BY Product ASC, TotalPrice DESC
LIMIT 15;


/* =================================================================================
   5. GROUP BY - category-wise analysis
   ================================================================================= */

-- 5.1 Number of orders placed for each product
SELECT Product, COUNT(*) AS OrderCount
FROM orders
GROUP BY Product
ORDER BY OrderCount DESC;

-- 5.2 Number of orders for each order status
SELECT OrderStatus, COUNT(*) AS OrderCount
FROM orders
GROUP BY OrderStatus
ORDER BY OrderCount DESC;


/* =================================================================================
   6. AGGREGATE FUNCTIONS - COUNT(), SUM(), AVG()
   ================================================================================= */

-- 6.1 Overall business snapshot in one query
SELECT COUNT(*)            AS TotalOrders,
       SUM(TotalPrice)     AS TotalRevenue,
       ROUND(AVG(TotalPrice), 2) AS AvgOrderValue,
       MIN(TotalPrice)     AS SmallestOrder,
       MAX(TotalPrice)     AS LargestOrder
FROM orders;

-- 6.2 Total quantity of items sold across all orders
SELECT SUM(Quantity) AS TotalUnitsSold
FROM orders;

-- 6.3 Average number of items customers keep in their cart
SELECT ROUND(AVG(ItemsInCart), 2) AS AvgItemsInCart
FROM orders;


/* =================================================================================
   7. PRODUCT-WISE ORDER COUNT AND SALES ANALYSIS
   ================================================================================= */

-- 7.1 For every product: how many orders, total revenue, and average order value
SELECT Product,
       COUNT(*)                  AS OrderCount,
       SUM(TotalPrice)           AS TotalRevenue,
       ROUND(AVG(TotalPrice), 2) AS AvgOrderValue,
       SUM(Quantity)             AS UnitsSold
FROM orders
GROUP BY Product
ORDER BY TotalRevenue DESC;


/* =================================================================================
   8. PAYMENT-METHOD-WISE ANALYSIS
   ================================================================================= */

-- 8.1 Orders, revenue, and average order value by payment method
SELECT PaymentMethod,
       COUNT(*)                  AS OrderCount,
       SUM(TotalPrice)           AS TotalRevenue,
       ROUND(AVG(TotalPrice), 2) AS AvgOrderValue
FROM orders
GROUP BY PaymentMethod
ORDER BY TotalRevenue DESC;


/* =================================================================================
   9. ORDER-STATUS-WISE ANALYSIS
   ================================================================================= */

-- 9.1 Orders, revenue, and average order value by order status
SELECT OrderStatus,
       COUNT(*)                  AS OrderCount,
       SUM(TotalPrice)           AS TotalRevenue,
       ROUND(AVG(TotalPrice), 2) AS AvgOrderValue
FROM orders
GROUP BY OrderStatus
ORDER BY OrderCount DESC;

-- 9.2 What share of ALL orders end up Cancelled or Returned? (a data-quality / ops signal)
SELECT OrderStatus, COUNT(*) AS OrderCount,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) AS PctOfAllOrders
FROM orders
WHERE OrderStatus IN ('Cancelled', 'Returned')
GROUP BY OrderStatus;


/* =================================================================================
   10. QUANTITY-WISE ANALYSIS
   ================================================================================= */

-- 10.1 How order count and revenue change as Quantity per order increases
SELECT Quantity,
       COUNT(*)                  AS OrderCount,
       SUM(TotalPrice)           AS TotalRevenue,
       ROUND(AVG(TotalPrice), 2) AS AvgOrderValue
FROM orders
GROUP BY Quantity
ORDER BY Quantity ASC;


/* =================================================================================
   11. REFERRAL-SOURCE-WISE ANALYSIS
   ================================================================================= */

-- 11.1 Orders, revenue and average order value generated by each marketing channel
SELECT ReferralSource,
       COUNT(*)                  AS OrderCount,
       SUM(TotalPrice)           AS TotalRevenue,
       ROUND(AVG(TotalPrice), 2) AS AvgOrderValue
FROM orders
GROUP BY ReferralSource
ORDER BY TotalRevenue DESC;


/* =================================================================================
   12. HAVING - filtering grouped results
   (HAVING filters groups AFTER aggregation; WHERE cannot filter on an aggregate)
   ================================================================================= */

-- 12.1 Only products with more than 170 orders (a "best sellers" cut-off)
SELECT Product, COUNT(*) AS OrderCount
FROM orders
GROUP BY Product
HAVING COUNT(*) > 170
ORDER BY OrderCount DESC;

-- 12.2 Only payment methods whose average order value exceeds $1,050
SELECT PaymentMethod, ROUND(AVG(TotalPrice), 2) AS AvgOrderValue
FROM orders
GROUP BY PaymentMethod
HAVING AVG(TotalPrice) > 1050
ORDER BY AvgOrderValue DESC;

-- 12.3 Only referral sources that generated more than $250,000 in total revenue
SELECT ReferralSource, SUM(TotalPrice) AS TotalRevenue
FROM orders
GROUP BY ReferralSource
HAVING SUM(TotalPrice) > 250000
ORDER BY TotalRevenue DESC;


/* =================================================================================
   13. PERCENTAGE CONTRIBUTION OF EACH PRODUCT/CATEGORY TO TOTAL SALES
   (a subquery in the denominator gives the grand total to divide into)
   ================================================================================= */

-- 13.1 Percentage of total revenue contributed by each product
SELECT Product,
       SUM(TotalPrice) AS Revenue,
       ROUND(SUM(TotalPrice) * 100.0 / (SELECT SUM(TotalPrice) FROM orders), 2) AS PctOfTotalSales
FROM orders
GROUP BY Product
ORDER BY PctOfTotalSales DESC;

-- 13.2 Percentage of total revenue contributed by each payment method
SELECT PaymentMethod,
       SUM(TotalPrice) AS Revenue,
       ROUND(SUM(TotalPrice) * 100.0 / (SELECT SUM(TotalPrice) FROM orders), 2) AS PctOfTotalSales
FROM orders
GROUP BY PaymentMethod
ORDER BY PctOfTotalSales DESC;

-- 13.3 Percentage of total revenue contributed by each referral source
SELECT ReferralSource,
       SUM(TotalPrice) AS Revenue,
       ROUND(SUM(TotalPrice) * 100.0 / (SELECT SUM(TotalPrice) FROM orders), 2) AS PctOfTotalSales
FROM orders
GROUP BY ReferralSource
ORDER BY PctOfTotalSales DESC;


/* =================================================================================
   BONUS: A FEW COMBINED / MULTI-CONCEPT QUERIES
   (SELECT + WHERE + GROUP BY + HAVING + ORDER BY together)
   ================================================================================= */

-- Products that are both popular (100+ orders) AND high-value (avg order > $1,000),
-- restricted to orders that were actually Delivered
SELECT Product,
       COUNT(*)                  AS DeliveredOrderCount,
       ROUND(AVG(TotalPrice), 2) AS AvgOrderValue
FROM orders
WHERE OrderStatus = 'Delivered'
GROUP BY Product
HAVING COUNT(*) >= 20 AND AVG(TotalPrice) > 1000
ORDER BY AvgOrderValue DESC;

/* =================================================================================
   END OF SCRIPT
   ================================================================================= */
