import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

st.set_page_config(
    page_title="Food Wastage Management System",
    layout="wide"
)

# Database Connection
from sqlalchemy import create_engine


engine = create_engine("mysql+pymysql://root:Ovs%40sql1@localhost:3306/food_wastage_management")


st.title("🍱 Local Food Wastage Management System")

menu = st.sidebar.selectbox(
    "Select Option",
    [
        "Dashboard",
        "Food Listings",
        "Providers",
        "Receivers",
        "Claims",
        "SQL Analysis"
    ]
)

# DASHBOARD
if menu == "Dashboard":

    st.header("Dashboard")

    food = pd.read_sql(
        "SELECT * FROM food_listings",
        engine
    )

    claims = pd.read_sql(
        "SELECT * FROM claims",
        engine
    )

    providers = pd.read_sql(
        "SELECT * FROM providers",
        engine
    )

    col1,col2,col3=st.columns(3)

    col1.metric(
        "Food Items",
        len(food)
    )

    col2.metric(
        "Providers",
        len(providers)
    )

    col3.metric(
        "Claims",
        len(claims)
    )

    city_data = food.groupby(
        "Location"
    )["Quantity"].sum().reset_index()

    fig = px.bar(
        city_data,
        x="Location",
        y="Quantity",
        title="Food Available by City"
    )

    st.plotly_chart(fig,use_container_width=True)

# FOOD FILTERING
elif menu=="Food Listings":

    st.header("Food Listings")

    food = pd.read_sql(
        "SELECT * FROM food_listings",
        engine
    )

    city = st.selectbox(
        "City",
        ["All"] + sorted(food["Location"].unique().tolist())
    )

    food_type = st.selectbox(
        "Food Type",
        ["All"] + sorted(food["Food_Type"].unique().tolist())
    )

    meal_type = st.selectbox(
        "Meal Type",
        ["All"] + sorted(food["Meal_Type"].unique().tolist())
    )

    filtered = food.copy()

    if city!="All":
        filtered=filtered[
            filtered["Location"]==city
        ]

    if food_type!="All":
        filtered=filtered[
            filtered["Food_Type"]==food_type
        ]

    if meal_type!="All":
        filtered=filtered[
            filtered["Meal_Type"]==meal_type
        ]

    st.dataframe(filtered)

# PROVIDERS
elif menu=="Providers":

    providers = pd.read_sql(
        "SELECT * FROM providers",
        engine
    )

    st.header("Providers")
    st.dataframe(providers)

# RECEIVERS
elif menu=="Receivers":

    receivers = pd.read_sql(
        "SELECT * FROM receivers",
        engine
    )

    st.header("Receivers")
    st.dataframe(receivers)

# CLAIMS
elif menu=="Claims":

    claims = pd.read_sql(
        "SELECT * FROM claims",
        engine
    )

    st.header("Claims")
    st.dataframe(claims)

# SQL ANALYSIS
elif menu=="SQL Analysis":

    st.header("SQL Analysis")

    queries = {
        "1. Providers by City":
        """
        SELECT City,
        COUNT(*) AS Provider_Count
        FROM providers
        GROUP BY City
        ORDER BY Provider_Count DESC
        """,

        "2. Receivers by City":
        """
        SELECT City,
        COUNT(*) AS Receiver_Count
        FROM receivers
        GROUP BY City
        ORDER BY Receiver_Count DESC
        """,

        "3. Food Contribution by Provider Type":
        """
        SELECT Provider_Type,
        SUM(Quantity) AS Total_Food
        FROM food_listings
        GROUP BY Provider_Type
        ORDER BY Total_Food DESC
        """,

        "4. Provider Contact Details":
        """
        SELECT Name,Type,Contact,City
        FROM providers
        """,

        "5. Receivers Claiming Most Food":
        """
        SELECT r.Name,
        COUNT(*) AS Claims
        FROM receivers r
        JOIN claims c
        ON r.Receiver_ID=c.Receiver_ID
        GROUP BY r.Name
        ORDER BY Claims DESC
        """,

        "6. Total Food Available":
        """
        SELECT SUM(Quantity)
        AS Total_Food
        FROM food_listings
        """,

        "7. City with Highest Listings":
        """
        SELECT Location,
        COUNT(*) AS Listings
        FROM food_listings
        GROUP BY Location
        ORDER BY Listings DESC
        """,

        "8. Most Common Food Types":
        """
        SELECT Food_Type,
        COUNT(*) AS Count_Food
        FROM food_listings
        GROUP BY Food_Type
        ORDER BY Count_Food DESC
        """,

        "9. Claims Per Food Item":
        """
        SELECT f.Food_Name,
        COUNT(c.Claim_ID) AS Claims
        FROM food_listings f
        LEFT JOIN claims c
        ON f.Food_ID=c.Food_ID
        GROUP BY f.Food_Name
        """,

        "10. Provider with Highest Successful Claims":
        """
        SELECT p.Name,
        COUNT(*) AS Successful_Claims
        FROM providers p
        JOIN food_listings f
        ON p.Provider_ID=f.Provider_ID
        JOIN claims c
        ON f.Food_ID=c.Food_ID
        WHERE c.Status='Completed'
        GROUP BY p.Name
        ORDER BY Successful_Claims DESC
        """,

        "11. Claim Status Percentage":
        """
        SELECT Status,
        ROUND(
        COUNT(*)*100/
        (SELECT COUNT(*) FROM claims),2
        ) AS Percentage
        FROM claims
        GROUP BY Status
        """,

        "12. Average Quantity Claimed":
        """
        SELECT r.Name,
        AVG(f.Quantity) AS Avg_Quantity
        FROM receivers r
        JOIN claims c
        ON r.Receiver_ID=c.Receiver_ID
        JOIN food_listings f
        ON c.Food_ID=f.Food_ID
        GROUP BY r.Name
        """,

        "13. Most Claimed Meal Type":
        """
        SELECT Meal_Type,
        COUNT(*) AS Claims
        FROM food_listings f
        JOIN claims c
        ON f.Food_ID=c.Food_ID
        GROUP BY Meal_Type
        ORDER BY Claims DESC
        """,

        "14. Quantity Donated by Provider":
        """
        SELECT p.Name,
        SUM(f.Quantity) AS Donated
        FROM providers p
        JOIN food_listings f
        ON p.Provider_ID=f.Provider_ID
        GROUP BY p.Name
        ORDER BY Donated DESC
        """,

        "15. Quantity by City":
        """
        SELECT Location,
        SUM(Quantity) AS Quantity
        FROM food_listings
        GROUP BY Location
        ORDER BY Quantity DESC
        """,

        "16. Food Expiring Soon":
        """
        SELECT *
        FROM food_listings
        ORDER BY Expiry_Date
        LIMIT 20
        """,

        "17. Food Quantity by Food Type":
        """
        SELECT Food_Type,
        SUM(Quantity) AS Quantity
        FROM food_listings
        GROUP BY Food_Type
        """,

        "18. Claim Status Count":
        """
        SELECT Status,
        COUNT(*) AS Total
        FROM claims
        GROUP BY Status
        """
    }
        

    selected = st.selectbox(
        "Choose Query",
        list(queries.keys())
    )

    result = pd.read_sql(
        queries[selected],
        engine
    )

    st.dataframe(result)