# Import python packages
import streamlit as st
import requests
import pandas as pd
#### from snowflake.snowpark.context import get_active_session  #####
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothies:cup_with_straw:")
st.write(
  """Choose the fruits you want in your Custom smoothies!""")


name_on_order=st.text_input('Name on Smoothie:')
st.write('Name on Smoothie will be',name_on_order)

###session=get_active_session()

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe=session.table("smoothies.public.fruit_options").select (col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#Convert snowflake Data frame to pandas data frame to use LOC function #
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list= st.multiselect(
    "choose upto 5 Ingredients?", 
      my_dataframe,
      max_selections=5)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)   
    
    ingredients_string=''
    
    for fruit_choosen  in  ingredients_list:
        ingredients_string+=fruit_choosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_choosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_choosen,' is ', search_on, '.')

        st.subheader(fruit_choosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
  
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    time_to_inser = st.button("Submit Order")
    #st.write(my_insert_stmt)
    #st.stop()

    if time_to_inser:
        session.sql(my_insert_stmt).collect()
        st.success("""Your Smoothie is ordered , """ + name_on_order + """!""", icon="✅")


smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
