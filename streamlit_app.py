import streamlit

streamlit.title('My parents New Healthy Diner')

streamlit.header('🍞Breakfast Menu')
streamlit.text('🫐Omega 3 & Blueberry Oatmeal')
streamlit.text('🫛Kale, Spinach & Rocket Smoothie')
streamlit.text('🥚Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json ())
  return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
#fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
#streamlit.write('The user entered ', fruit_choice)

import requests
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")

#take json format and normalise it 
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#output it on screen as a table
#streamlit.dataframe(fruityvice_normalized)

#streamlit.stop()

import snowflake.connector

streamlit.header("The fruit load list contains :")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()
    
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  #my_cur = my_cnx.cursor()
  #my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
  my_data_row = get_fruit_load_list()
  #streamlit.text("Hello from Snowflake:")
  #streamlit.text(my_data_row)
  #my_cur.execute("select * from fruit_load_list")
  #my_data_row = my_cur.fetchall()
  #streamlit.header("The fruit load list contains:")
  streamlit.dataframe(my_data_row)

def insert_row_now(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('from streamlit')")
    return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like information about?')
if streamlit.button('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  #my_cur = my_cnx.cursor()
  #my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
  back_from_function = insert_row_now(add_my_fruit)
  #streamlit.text("Hello from Snowflake:")
  #streamlit.text(my_data_row)
  #my_cur.execute("select * from fruit_load_list")
  #my_data_row = my_cur.fetchall()
  #streamlit.header("The fruit load list contains:")
  streamlit.dataframe(back_from_function)
#fruit_choice1 = streamlit.text_input('What fruit would you like information about?','jackfruit')
#streamlit.write('Thanks for adding ', fruit_choice1)

#my_cur.execute("insert into fruit_load_list values ('from streamlit')")
  
try:
  fruit_choice = streamlit.text_input ('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error("Please select a fruit to get information. ")
  else:
      back_from_function = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()
