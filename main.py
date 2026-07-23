# STEP 1A
# Import SQL Library and Pandas
import sqlite3
import pandas as pd

# STEP 1B
# Connect to the database
conn = sqlite3.connect('data.sqlite')

# STEP 2
# Replace None with your code
df_first_five = pd.read_sql("""
SELECT firstName, lastName, jobTitle
FROM employees
JOIN offices
    USING (officeCode)
WHERE offices.city = 'Boston'    
""", conn)
print (df_first_five)

# STEP 3
# Replace None with your code
df_five_reverse = pd.read_sql("""
SELECT officeCode, city
FROM offices
LEFT JOIN employees
    USING (officeCode)
WHERE employeeNumber IS NULL
""", conn)
print (df_five_reverse)

# STEP 4
# Replace None with your code
df_alias = pd.read_sql("""
SELECT firstName,lastName, city, state
FROM employees
LEFT JOIN offices
    USING (officeCode)
    ORDER BY lastName, firstName 
""", conn)
print (df_alias)

# STEP 5
# Replace None with your code
df_executive = pd.read_sql("""
SELECT contactFirstName, contactLastName, phone, salesRepEmployeeNumber
FROM customers
LEFT JOIN orders
    USING (customerNumber)
WHERE orderNumber IS NULL
ORDER BY contactLastName
""", conn)
print (df_executive)


# STEP 6
# Replace None with your code
df_name_length = pd.read_sql("""
SELECT contactFirstName, contactLastName, amount, paymentDate
FROM customers
JOIN payments
    USING (customerNumber)
ORDER BY CAST (amount AS REAL) DESC
""", conn)
print (df_name_length)


# STEP 7
# Replace None with your code
df_short_title = pd.read_sql("""
SELECT firstName, lastName, COUNT(customerNumber) AS numCustomers
FROM employees
JOIN customers
ON employeeNumber = salesRepEmployeeNumber
GROUP BY employeeNumber, firstName, lastName
HAVING AVG(creditLimit) > 90000
ORDER BY numCustomers DESC;
""", conn)
print (df_short_title)
# STEP 8
# Replace None with your code
sum_total_price = pd.read_sql("""
SELECT
    productName,
    COUNT(orderNumber) AS numorders,
    SUM(quantityOrdered) AS totalunits
FROM products
JOIN orderDetails
USING (productCode)
GROUP BY productCode, productName
ORDER BY totalunits DESC;
""", conn).iloc[:, 0]
print (sum_total_price)

# STEP 9
# Replace None with your code
df_day_month_year = pd.read_sql("""
SELECT
    productName,
    productCode,
    COUNT(DISTINCT customerNumber) AS numpurchasers
FROM products
JOIN orderDetails
USING (productCode)
JOIN orders
USING (orderNumber)
JOIN customers
USING (customerNumber)
GROUP BY productCode, productName
ORDER BY numpurchasers DESC;
""", conn)
print (df_day_month_year)


df_office_customers = pd.read_sql("""
SELECT
    offices.officeCode,
    offices.city,
    COUNT(customerNumber) AS n_customers
FROM offices
JOIN employees
USING (officeCode)
JOIN customers
ON employeeNumber = salesRepEmployeeNumber
GROUP BY offices.officeCode, offices.city;
""", conn)
print (df_office_customers)


df_product_sales = pd.read_sql("""
SELECT DISTINCT
    employeeNumber,
    firstName,
    lastName,
    offices.city,
    officeCode
FROM employees
JOIN offices
USING (officeCode)
JOIN customers
ON employeeNumber = salesRepEmployeeNumber
JOIN orders
USING (customerNumber)
JOIN orderDetails
USING (orderNumber)
WHERE productCode IN (
    SELECT productCode
    FROM orderDetails
    JOIN orders
    USING (orderNumber)
    GROUP BY productCode
    HAVING COUNT(DISTINCT customerNumber) < 20
);
""", conn)
print (df_product_sales)

conn.close()