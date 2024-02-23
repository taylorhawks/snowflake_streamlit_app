# coding from snowflake tutorial

import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

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

streamlit.dataframe(fruits_to_show)

### fruityvice ###

def get_fruityvice_data(this_fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
   fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
   return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
   else:
      back_from_function = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
except:
   pass
      



streamlit.header('Snowflake Connection')

if streamlit.button('Get Fruit Load List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_cur = my_cnx.cursor()
   my_cur.execute("SELECT * FROM fruit_load_list")
   my_data_row = my_cur.fetchall()
   streamlit.header("The fruit load list contains:")
   streamlit.dataframe(my_data_row)

def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur:
      my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
      return 'Thanks for adding' + new_fruit

add_my_fruit = ''

if streamlit.button('Add a Fruit to the List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   add_my_fruit = streamlit.text_input('Which fruit would you like to add?','')
   ret_val = insert_row_snowflake(add_my_fruit)
if len(add_my_fruit) > 0:
   streamlit.text(ret_val)
