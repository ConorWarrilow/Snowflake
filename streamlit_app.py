# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title("Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)

from snowflake.snowpark.functions import col

name_on_order = st.text_input('Name on smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)


#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table('SMOOTHIES.PUBLIC.FRUIT_OPTIONS').select(col('FRUIT_NAME')) # just the fruit name column
st.dataframe(data = my_dataframe, use_container_width = True)


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', my_dataframe, max_selections = 5
)


if ingredients_list:
    #ingredients_string variable to populate our orders table
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)

    # Were essentially writing our SQL code right here
    # we need to comment out the text we want as our SQL code, and also make sure we 
    #comment out a comma between our ingredients and name, essentially creating a big string
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '"""+name_on_order+"""')"""

    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success(f"{name_on_order}, Your smoothie is ordered!", icon="✅")


import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response.json())
