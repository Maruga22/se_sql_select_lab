# STEP 1A
# Import SQL Library and Pandas
import sqlite3
import pandas as pd

# STEP 1B
# Connect to the database
conn = sqlite3.connect('data.sqlite')

df_boston = pd.read_sql("""
SELECT firstName, lastName
FROM employees
JOIN offices USING (officeCode)
WHERE offices.city = 'Boston'
""", conn)

df_employee = pd.read_sql("""
SELECT firstName, lastName, city, state
FROM employees
LEFT JOIN offices USING (officeCode)
ORDER BY lastName, firstName
""", conn)

df_customer_payment = pd.read_sql("""
SELECT contactFirstName, contactLastName, amount, paymentDate
FROM customers
JOIN payments USING (customerNumber)
ORDER BY CAST(amount AS REAL) DESC
""", conn)

df_credit = pd.read_sql("""
SELECT firstName, lastName, COUNT(customerNumber) AS numCustomers
FROM employees
JOIN customers ON employeeNumber = salesRepEmployeeNumber
GROUP BY employeeNumber, firstName, lastName
HAVING AVG(creditLimit) > 90000
ORDER BY numCustomers DESC
""", conn)

df_product_customers = pd.read_sql("""
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

df_under_20 = pd.read_sql("""
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

conn.close()