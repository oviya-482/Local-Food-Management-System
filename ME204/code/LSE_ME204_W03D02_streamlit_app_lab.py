import sqlite3

import pandas as pd

# Altair is a dataviz library that also adhers to the Grammar of Graphics
import altair as alt
import streamlit as st


# Creating a connection to the database
conn = sqlite3.connect('../data/supermarket.db')

# Querying the database to get the categories
BASE_CATEGORIES_QUERY = (
'''
SELECT 
    name || ' (' || COUNT(*) || ')' as category
FROM categories
GROUP BY name
ORDER BY COUNT(*) DESC
'''
)

BASE_PRODUCT_QUERY = (
'''
SELECT 
    prod.id as product_id, 
    prod.name as product_name,
    prod.size as product_size,
    prc.`item-price` as price,
    prc.`price-per-unit` as price_per_unit,
    off.`offer-description` as offer_description,
    CASE
        WHEN off.`offer-description` IS NULL THEN 'No offer'
        ELSE 'HAS OFFER'
    END as has_offer,
    GROUP_CONCAT(DISTINCT cat.name) as categories
FROM products prod
LEFT JOIN prices prc
ON prod.id = prc.product_id
LEFT JOIN offers off
ON prod.id = off.product_id
LEFT JOIN categories cat
ON prod.id = cat.product_id
WHERE 
    prod.name LIKE "%{search_term}%"
GROUP BY prod.id
HAVING categories LIKE "%{category}%"
''')

def highlight_offers(row):
    if row['has_offer'] == 'HAS OFFER':
        # Use background-color #3995BA and font color white
        return ['background-color: #3995BA; color: white']*len(row)
    else:
        return ['background-color: white']*len(row)


def app():

    st.set_page_config(
        page_title="Explore Products by Name",
        layout="wide" 
    )


    # Add two columns: left-hand side to get text input and right-hand side to view the data
    col1, col2 = st.columns([1, 2])

    with col1:
        st.write('Type part of a product name to search for it in the database')
        search_term = st.text_input('Search for a product')

        # Filter by category (optional)
        st.write('Filter by category')
        if search_term == '': 
            categories = pd.read_sql(BASE_CATEGORIES_QUERY, conn)
        else:
            products = pd.read_sql(BASE_PRODUCT_QUERY.format(search_term=search_term, category=''), conn)
            if products.empty:
                categories = pd.DataFrame()
                st.error('No products found for the search term. Please try again.')
            else:
                categories = (
                    products['categories'].str.split(',', expand=True).stack()
                        .value_counts().reset_index()
                        .rename(columns={'index': 'category'})
                )
                categories['category'] = categories.apply(lambda x: x['category'] + f' ({x["count"]})', axis=1)

        if categories.empty:
            category = None
        else:
            category = st.selectbox('Select a category', categories['category'], index=None)
        


    with col2:

        if search_term == '': 
            st.markdown('👈 **Please type a product name to search for it in the database**')
        elif search_term != '' and not categories.empty:
            # with st.spinner('Searching for products...'):
            st.markdown('## Product list')
            st.write(products.shape[0], 'matching products found for query:', search_term)
            # Querying the database to get the products
            if search_term == '':
                products = pd.DataFrame()
            elif category is None:
                products = pd.read_sql(BASE_PRODUCT_QUERY.format(search_term=search_term, category=''), conn)
            else:
                category = category.split('(')[0].strip()
                products = pd.read_sql(BASE_PRODUCT_QUERY.format(search_term=search_term, category=category), conn)

            products['offer_description'] = products['offer_description'].fillna('No offer')
            # Display the data
            st.dataframe(products.style.apply(highlight_offers, axis=1))

            ### MELT THE DATAFRAME BASED ON THE CATEGORIES
            products = (
                products.assign(categories=products['categories'].str.split(','))
                        .explode('categories')
                        .rename(columns={'categories': 'category'})
            )

            # Display the scatterplot
            st.markdown('## Price vs Offer')
            scatterplot = alt.Chart(products).mark_circle(size=90, stroke='black', opacity=0.5, strokeWidth=1).encode(
                x=alt.X('price:Q', title='Price',axis=alt.Axis(format='$.2f')),
                y=alt.Y('category:N', title='Categories'),
                yOffset='jitter:Q',
                color=alt.Color('has_offer:N', 
                                title='Offer', 
                                scale=alt.Scale(domain=['HAS OFFER', 'No offer'], 
                                                range=['#3995BA', '#F8CE0A'])),
                tooltip=[alt.Tooltip('product_name', title='Product'),
                         # Format with GBP
                        alt.Tooltip('price:Q', title='Price', format='$.2f'),
                        alt.Tooltip('offer_description', title='Offer')]
            ).transform_calculate(
                # Source: https://altair-viz.github.io/gallery/strip_plot_jitter.html
                jitter="sqrt(-2*log(random()))*cos(2*PI*random())"
            ).properties(
                width=800,
                height=400
            ).configure_axis(
                labelFontSize=13,
                titleFontSize=15
            )
            st.altair_chart(scatterplot, use_container_width=True)



if __name__ == '__main__':
    app()



