#created the main python  file
import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError



streamlit.title('My Parent New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free Range Egg')
streamlit.text('🥑🍞 avacado toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)


#New section to display fruityvice api response


def get_fruityvice_data(this_fruit_choice):
  #streamlit.text(fruityvice_response.json()) #just write the data to the screen  #we delete this line to get rid of json 
  # Take the json version of response and normalize it
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())  
  return fruityvice_normalized

streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please select a fruit name to get information')
  else:
    back_from_function=get_fruityvice_data(fruit_choice)
# Output it the screen as a table
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

#Don't run anything past here while we troubleshoot
# streamlit.stop()

# import snowflake.connector
streamlit.header("The fruit load list contains:")
#Snowflake-Related Functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
    return my_cur.fetchall()

#Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

# Allow the user to add fruits to the list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values('from streamlit')")
    return "Thanks for adding"+new_fruit
  
if streamlit.button('Add fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function= insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)  


# add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')

