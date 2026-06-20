
# 🍱 Local Food Wastage Management System
## Project link https://local-food-management-system-bjnx7ozmgge2srttn6d7mr.streamlit.app/
## 📌 Project Overview

The **Local Food Wastage Management System** is a data-driven web application developed using **Python, MySQL, and Streamlit** to reduce food wastage by connecting food providers with individuals and organizations in need.

The system enables food providers to list surplus food, while receivers can search, claim, and contact providers directly through the platform. The project also provides analytical insights into food donation patterns using SQL queries and interactive visualizations.

---

## 🎯 Objectives

* Reduce food wastage by redistributing surplus food.
* Connect food providers and receivers through a centralized platform.
* Analyze donation and claim trends using SQL and data visualization.
* Provide an easy-to-use interface for managing food donations.

---

## 🛠️ Technologies Used

| Technology   | Purpose                    |
| ------------ | -------------------------- |
| Python       | Backend Logic              |
| Streamlit    | Web Application            |
| MySQL        | Database Management        |
| SQLAlchemy   | Database Connectivity      |
| Pandas       | Data Manipulation          |
| Plotly       | Interactive Visualizations |
| PyMySQL      | MySQL Connector            |
| Git & GitHub | Version Control            |

---

## 📂 Dataset Description

The project uses four datasets:

### 1. Providers Dataset

Contains details of food providers.

| Column      |
| ----------- |
| Provider_ID |
| Name        |
| Type        |
| Address     |
| City        |
| Contact     |

---

### 2. Receivers Dataset

Contains details of food receivers.

| Column      |
| ----------- |
| Receiver_ID |
| Name        |
| Type        |
| City        |
| Contact     |

---

### 3. Food Listings Dataset

Contains available food donation details.

| Column        |
| ------------- |
| Food_ID       |
| Food_Name     |
| Quantity      |
| Expiry_Date   |
| Provider_ID   |
| Provider_Type |
| Location      |
| Food_Type     |
| Meal_Type     |

---

### 4. Claims Dataset

Contains claim information.

| Column      |
| ----------- |
| Claim_ID    |
| Food_ID     |
| Receiver_ID |
| Status      |
| Timestamp   |

---

## ✨ Features

### 🍲 Food Donation Management

* View available food donations.
* Filter donations based on:

  * Location
  * Provider
  * Food Type
  * Meal Type

---

### 📞 Contact Module

* View provider contact details.
* View receiver contact details.
* Contact providers and receivers directly through the application.

---

### 📝 CRUD Operations

Users can:

* ➕ Add new food listings
* ✏️ Update existing food listings
* ❌ Delete food listings

---

### 📊 Interactive Dashboard

Dashboard provides:

* Total Food Listings
* Total Providers
* Total Receivers
* Total Claims
* Food Quantity by City
* Food Type Distribution
* Meal Type Distribution
* Claim Status Distribution

---

## 📈 SQL Business Queries

The application answers the following business questions:

1. Number of providers in each city.
2. Number of receivers in each city.
3. Food contribution by provider type.
4. Provider contact details.
5. Top receivers based on claims.
6. Total food available.
7. City with the highest food listings.
8. Most common food types.
9. Claims per food item.
10. Providers with the highest successful claims.
11. Claim status percentages.
12. Average quantity claimed by receivers.
13. Most claimed meal type.
14. Quantity donated by each provider.
15. Food quantity distribution by city.

### Additional Queries

16. Food items expiring soon.
17. Quantity available by food type.
18. Claim status count.

---

## 🗄️ Database Schema

### Providers

```sql
Provider_ID (PK)
Name
Type
Address
City
Contact
```

### Receivers

```sql
Receiver_ID (PK)
Name
Type
City
Contact
```

### Food Listings

```sql
Food_ID (PK)
Food_Name
Quantity
Expiry_Date
Provider_ID (FK)
Provider_Type
Location
Food_Type
Meal_Type
```

### Claims

```sql
Claim_ID (PK)
Food_ID (FK)
Receiver_ID (FK)
Status
Timestamp
```

---

## ⚙️ Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/Local-Food-Wastage-Management-System.git
```

### Step 2: Navigate to Project Folder

```bash
cd Local-Food-Wastage-Management-System
```

### Step 3: Install Required Libraries

```bash
pip install -r requirements.txt
```

---

## 📦 Required Libraries

Create a `requirements.txt` file containing:

```txt
streamlit
pandas
plotly
sqlalchemy
pymysql
```

---

## 🛢️ Database Setup

1. Open MySQL Workbench.
2. Create the database:

```sql
CREATE DATABASE food_wastage_management;
USE food_wastage_management;
```

3. Execute the SQL script:

```sql
food_wastage_complete.sql
```

4. Import all datasets into MySQL tables.

---

## ▶️ Running the Application

Run the Streamlit application:

```bash
streamlit run food.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## 📸 Application Modules

* Dashboard
* Food Listings
* Provider Contacts
* Receiver Contacts
* CRUD Operations
* SQL Analysis

---

## 🚀 Future Enhancements

* User Authentication
* Email Notifications
* Real-time Chat System
* Food Claim Approval Workflow
* Google Maps Integration
* Cloud Deployment
* Mobile Application Support

---

## 👩‍💻 Author

**Oviya S**

Business Analytics Student | Aspiring Business Analyst

---

## 🙏 Acknowledgement

This project was developed as part of the internship project to demonstrate skills in:

* SQL
* Python
* Streamlit
* Data Analysis
* Database Management
* Data Visualization

