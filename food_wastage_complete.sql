
-- =====================================================
-- LOCAL FOOD WASTAGE MANAGEMENT SYSTEM
-- Complete MySQL Script
-- =====================================================

DROP DATABASE IF EXISTS food_wastage_management;
CREATE DATABASE food_wastage_management;
USE food_wastage_management;

-- =====================================================
-- TABLE CREATION
-- =====================================================

CREATE TABLE providers (
    Provider_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Type VARCHAR(100),
    Address TEXT,
    City VARCHAR(100),
    Contact VARCHAR(100)
);

CREATE TABLE receivers (
    Receiver_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Type VARCHAR(100),
    City VARCHAR(100),
    Contact VARCHAR(100)
);

CREATE TABLE food_listings (
    Food_ID INT PRIMARY KEY,
    Food_Name VARCHAR(255),
    Quantity INT,
    Expiry_Date DATE,
    Provider_ID INT,
    Provider_Type VARCHAR(100),
    Location VARCHAR(100),
    Food_Type VARCHAR(100),
    Meal_Type VARCHAR(100),
    FOREIGN KEY (Provider_ID) REFERENCES providers(Provider_ID)
);

CREATE TABLE claims (
    Claim_ID INT PRIMARY KEY,
    Food_ID INT,
    Receiver_ID INT,
    Status VARCHAR(50),
    Timestamp DATETIME,
    FOREIGN KEY (Food_ID) REFERENCES food_listings(Food_ID),
    FOREIGN KEY (Receiver_ID) REFERENCES receivers(Receiver_ID)
);

-- =====================================================
-- DATA IMPORT
-- Separate file with the insert commands
-- =====================================================

-- =====================================================
-- DATA CLEANING / MANIPULATION
-- =====================================================

UPDATE claims
SET Status = TRIM(Status);

UPDATE providers
SET City = TRIM(City);

UPDATE receivers
SET City = TRIM(City);

DELETE FROM food_listings
WHERE Quantity <= 0;

-- =====================================================
-- QUERY 1
-- Food providers in each city
-- =====================================================
SELECT City, COUNT(*) AS Provider_Count
FROM providers
GROUP BY City
ORDER BY Provider_Count DESC;

-- QUERY 2
SELECT City, COUNT(*) AS Receiver_Count
FROM receivers
GROUP BY City
ORDER BY Receiver_Count DESC;

-- QUERY 3
SELECT Provider_Type,
SUM(Quantity) AS Total_Food_Contributed
FROM food_listings
GROUP BY Provider_Type
ORDER BY Total_Food_Contributed DESC;

-- QUERY 4
SELECT Name, Type, Contact, City
FROM providers
WHERE City='New Jessica';

-- QUERY 5
SELECT r.Name,
COUNT(c.Claim_ID) AS Total_Claims
FROM receivers r
JOIN claims c
ON r.Receiver_ID=c.Receiver_ID
GROUP BY r.Receiver_ID,r.Name
ORDER BY Total_Claims DESC;

-- QUERY 6
SELECT SUM(Quantity) AS Total_Food_Available
FROM food_listings;

-- QUERY 7
SELECT Location,
COUNT(*) AS Food_Listings
FROM food_listings
GROUP BY Location
ORDER BY Food_Listings DESC;

-- QUERY 8
SELECT Food_Type,
COUNT(*) AS Available_Count
FROM food_listings
GROUP BY Food_Type
ORDER BY Available_Count DESC;

-- QUERY 9
SELECT f.Food_Name,
COUNT(c.Claim_ID) AS Number_Of_Claims
FROM food_listings f
LEFT JOIN claims c
ON f.Food_ID=c.Food_ID
GROUP BY f.Food_ID,f.Food_Name
ORDER BY Number_Of_Claims DESC;

-- QUERY 10
SELECT p.Name,
COUNT(*) AS Successful_Claims
FROM providers p
JOIN food_listings f
ON p.Provider_ID=f.Provider_ID
JOIN claims c
ON f.Food_ID=c.Food_ID
WHERE c.Status='Completed'
GROUP BY p.Provider_ID,p.Name
ORDER BY Successful_Claims DESC;

-- QUERY 11
SELECT Status,
ROUND(COUNT(*)*100.0/
(SELECT COUNT(*) FROM claims),2) AS Percentage
FROM claims
GROUP BY Status;

-- QUERY 12
SELECT r.Name,
ROUND(AVG(f.Quantity),2) AS Avg_Quantity_Claimed
FROM receivers r
JOIN claims c
ON r.Receiver_ID=c.Receiver_ID
JOIN food_listings f
ON c.Food_ID=f.Food_ID
GROUP BY r.Receiver_ID,r.Name
ORDER BY Avg_Quantity_Claimed DESC;

-- QUERY 13
SELECT Meal_Type,
COUNT(*) AS Total_Claims
FROM food_listings f
JOIN claims c
ON f.Food_ID=c.Food_ID
GROUP BY Meal_Type
ORDER BY Total_Claims DESC;

-- QUERY 14
SELECT p.Name,
SUM(f.Quantity) AS Total_Donated
FROM providers p
JOIN food_listings f
ON p.Provider_ID=f.Provider_ID
GROUP BY p.Provider_ID,p.Name
ORDER BY Total_Donated DESC;

-- QUERY 15
SELECT Location,
SUM(Quantity) AS Total_Food_By_City
FROM food_listings
GROUP BY Location
ORDER BY Total_Food_By_City DESC;

-- QUERY 16
SELECT Food_Name, Quantity, Expiry_Date
FROM food_listings
ORDER BY Expiry_Date;

-- QUERY 17
SELECT Food_Type,
SUM(Quantity) AS Quantity
FROM food_listings
GROUP BY Food_Type;

-- QUERY 18
SELECT Status,
COUNT(*) AS Total_Claims
FROM claims
GROUP BY Status;
