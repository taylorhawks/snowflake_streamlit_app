# coding from snowflake tutorial

import streamlit
import pandas as pd
import requests
import snowflake.connector

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt").set_index('Fruit')

streamlit.title('My Parents New Healthy Diner')

   # emojis might not render properly

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')


#smoothies
streamlit.header('Build Your Own Smoothie')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected] #use indices of selected fruits

# Display the table on the page.


streamlit.dataframe(fruits_to_show)

#fruityvice
streamlit.header("Fruityvice Fruit Advice!")

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# # streamlit.text(fruityvice_response.json())

# put the json into pandas df
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# display the df
streamlit.dataframe(fruityvice_normalized)

streamlit.header('Snowflake Connection')

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)
