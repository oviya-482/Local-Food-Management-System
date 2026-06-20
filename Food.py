import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# ==================================================
# DATABASE CONNECTION
# ==================================================



engine = create_engine(
    f"mysql+pymysql://root:Ovs%40sql1@localhost:3306/food_wastage_management"
)

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Local Food Wastage Management System",
    layout="wide"
)

st.title("🍱 Local Food Wastage Management System")

# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_food():
    return pd.read_sql("SELECT * FROM food_listings", engine)

@st.cache_data
def load_providers():
    return pd.read_sql("SELECT * FROM providers", engine)

@st.cache_data
def load_receivers():
    return pd.read_sql("SELECT * FROM receivers", engine)

@st.cache_data
def load_claims():
    return pd.read_sql("SELECT * FROM claims", engine)

# ==================================================
# SIDEBAR
# ==================================================

menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Dashboard",
        "Food Listings",
        "Provider Contacts",
        "Receiver Contacts",
        "CRUD Operations",
        "SQL Analysis"
    ]
)

# ==================================================
# DASHBOARD
# ==================================================

if menu == "Dashboard":

    food = load_food()
    providers = load_providers()
    receivers = load_receivers()
    claims = load_claims()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Food Listings", len(food))
    col2.metric("Providers", len(providers))
    col3.metric("Receivers", len(receivers))
    col4.metric("Claims", len(claims))

    st.divider()

    st.subheader("Food Quantity by City")

    city_qty = (
        food.groupby("Location")["Quantity"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        city_qty,
        x="Location",
        y="Quantity"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Food Type Distribution")

    fig2 = px.pie(
        food,
        names="Food_Type"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Meal Type Distribution")

    fig3 = px.histogram(
        food,
        x="Meal_Type"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Claim Status Distribution")

    fig4 = px.pie(
        claims,
        names="Status"
    )

    st.plotly_chart(fig4, use_container_width=True)

# ==================================================
# FOOD LISTINGS
# ==================================================

elif menu == "Food Listings":

    food = load_food()

    st.subheader("Filter Food Donations")

    city = st.selectbox(
        "Location",
        ["All"] + sorted(food["Location"].dropna().unique().tolist())
    )

    provider = st.selectbox(
        "Provider Type",
        ["All"] + sorted(food["Provider_Type"].dropna().unique().tolist())
    )

    food_type = st.selectbox(
        "Food Type",
        ["All"] + sorted(food["Food_Type"].dropna().unique().tolist())
    )

    meal_type = st.selectbox(
        "Meal Type",
        ["All"] + sorted(food["Meal_Type"].dropna().unique().tolist())
    )

    filtered = food.copy()

    if city != "All":
        filtered = filtered[
            filtered["Location"] == city
        ]

    if provider != "All":
        filtered = filtered[
            filtered["Provider_Type"] == provider
        ]

    if food_type != "All":
        filtered = filtered[
            filtered["Food_Type"] == food_type
        ]

    if meal_type != "All":
        filtered = filtered[
            filtered["Meal_Type"] == meal_type
        ]

    st.dataframe(filtered)

# ==================================================
# PROVIDER CONTACTS
# ==================================================

elif menu == "Provider Contacts":

    providers = load_providers()

    selected = st.selectbox(
        "Select Provider",
        providers["Name"].unique()
    )

    result = providers[
        providers["Name"] == selected
    ]

    st.dataframe(result)
    
    phone = str(result.iloc[0]["Contact"])

    st.markdown(
    f"[💬 WhatsApp Provider](https://wa.me/91{phone})"
)

# ==================================================
# RECEIVER CONTACTS
# ==================================================

elif menu == "Receiver Contacts":

    receivers = load_receivers()

    selected = st.selectbox(
        "Select Receiver",
        receivers["Name"].unique()
    )

    result = receivers[
        receivers["Name"] == selected
    ]

    st.dataframe(result)

    phone = str(result.iloc[0]["Contact"])

    st.markdown(
    f"[💬 WhatsApp Receiver](https://wa.me/91{phone})"
)

# ==================================================
# CRUD
# ==================================================

elif menu == "CRUD Operations":

    st.header("Food Listing CRUD")

    crud_option = st.radio(
        "Choose Action",
        ["Add", "Update", "Delete"]
    )

    # ADD
    if crud_option == "Add":

        st.subheader("Add Food Listing")

        with st.form("add_form"):

            food_id = st.number_input("Food ID", step=1)

            food_name = st.text_input("Food Name")

            quantity = st.number_input(
                "Quantity",
                min_value=1
            )

            provider_id = st.number_input(
                "Provider ID",
                step=1
            )

            submit = st.form_submit_button("Add")

            if submit:

                sql = text("""
                INSERT INTO food_listings
                (Food_ID, Food_Name, Quantity, Provider_ID)
                VALUES
                (:food_id,:food_name,:quantity,:provider_id)
                """)

                with engine.begin() as conn:
                    conn.execute(
                        sql,
                        {
                            "food_id": int(food_id),
                            "food_name": food_name,
                            "quantity": int(quantity),
                            "provider_id": int(provider_id)
                        }
                    )

                st.success("Record Added")

    # UPDATE
    elif crud_option == "Update":

        st.subheader("Update Food Quantity")

        food_id = st.number_input(
            "Food ID",
            step=1
        )

        quantity = st.number_input(
            "New Quantity",
            step=1
        )

        if st.button("Update"):

            sql = text("""
            UPDATE food_listings
            SET Quantity=:qty
            WHERE Food_ID=:food_id
            """)

            with engine.begin() as conn:
                conn.execute(
                    sql,
                    {
                        "qty": int(quantity),
                        "food_id": int(food_id)
                    }
                )

            st.success("Updated")

    # DELETE
    else:

        st.subheader("Delete Food Listing")

        food_id = st.number_input(
            "Food ID",
            step=1
        )

        if st.button("Delete"):

            sql = text("""
            DELETE FROM food_listings
            WHERE Food_ID=:food_id
            """)

            with engine.begin() as conn:
                conn.execute(
                    sql,
                    {
                        "food_id": int(food_id)
                    }
                )

            st.success("Deleted")

# ==================================================
# SQL ANALYSIS
# ==================================================

elif menu == "SQL Analysis":

    queries = {

        "1 Providers by City":
        """
        SELECT City,COUNT(*) Provider_Count
        FROM providers
        GROUP BY City
        ORDER BY Provider_Count DESC
        """,

        "2 Receivers by City":
        """
        SELECT City,COUNT(*) Receiver_Count
        FROM receivers
        GROUP BY City
        ORDER BY Receiver_Count DESC
        """,

        "3 Food Contribution by Provider Type":
        """
        SELECT Provider_Type,
        SUM(Quantity) Total_Food
        FROM food_listings
        GROUP BY Provider_Type
        """,

        "4 Provider Contacts":
        """
        SELECT Name,Type,Contact,City
        FROM providers
        """,

        "5 Top Receivers":
        """
        SELECT r.Name,
        COUNT(*) Claims
        FROM receivers r
        JOIN claims c
        ON r.Receiver_ID=c.Receiver_ID
        GROUP BY r.Name
        ORDER BY Claims DESC
        """,

        "6 Total Food Available":
        """
        SELECT SUM(Quantity) Total_Food
        FROM food_listings
        """,

        "7 City with Highest Listings":
        """
        SELECT Location,
        COUNT(*) Listings
        FROM food_listings
        GROUP BY Location
        ORDER BY Listings DESC
        """,

        "8 Most Common Food Types":
        """
        SELECT Food_Type,
        COUNT(*) Count_Food
        FROM food_listings
        GROUP BY Food_Type
        ORDER BY Count_Food DESC
        """,

        "9 Claims Per Food Item":
        """
        SELECT f.Food_Name,
        COUNT(c.Claim_ID) Claims
        FROM food_listings f
        LEFT JOIN claims c
        ON f.Food_ID=c.Food_ID
        GROUP BY f.Food_Name
        """,

        "10 Successful Claims by Provider":
        """
        SELECT p.Name,
        COUNT(*) Successful_Claims
        FROM providers p
        JOIN food_listings f
        ON p.Provider_ID=f.Provider_ID
        JOIN claims c
        ON f.Food_ID=c.Food_ID
        WHERE c.Status='Completed'
        GROUP BY p.Name
        """,

        "11 Claim Status Percentage":
        """
        SELECT Status,
        ROUND(
        COUNT(*)*100/
        (SELECT COUNT(*) FROM claims),2
        ) Percentage
        FROM claims
        GROUP BY Status
        """,

        "12 Average Quantity Claimed":
        """
        SELECT r.Name,
        AVG(f.Quantity) Avg_Quantity
        FROM receivers r
        JOIN claims c
        ON r.Receiver_ID=c.Receiver_ID
        JOIN food_listings f
        ON c.Food_ID=f.Food_ID
        GROUP BY r.Name
        """,

        "13 Most Claimed Meal Type":
        """
        SELECT Meal_Type,
        COUNT(*) Claims
        FROM food_listings f
        JOIN claims c
        ON f.Food_ID=c.Food_ID
        GROUP BY Meal_Type
        """,

        "14 Quantity Donated by Provider":
        """
        SELECT p.Name,
        SUM(f.Quantity) Donated
        FROM providers p
        JOIN food_listings f
        ON p.Provider_ID=f.Provider_ID
        GROUP BY p.Name
        """,

        "15 Quantity by City":
        """
        SELECT Location,
        SUM(Quantity) Quantity
        FROM food_listings
        GROUP BY Location
        """,

        "16 Food Expiring Soon":
        """
        SELECT *
        FROM food_listings
        ORDER BY Expiry_Date
        LIMIT 20
        """,

        "17 Quantity by Food Type":
        """
        SELECT Food_Type,
        SUM(Quantity) Quantity
        FROM food_listings
        GROUP BY Food_Type
        """,

        "18 Claim Status Count":
        """
        SELECT Status,
        COUNT(*) Total
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