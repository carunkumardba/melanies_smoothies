# Import python packages
import streamlit as st
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

my_dataframe=session.table("smoothies.public.fruit_options").select (col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list= st.multiselect(
    "choose upto 5 Ingredients?", my_dataframe,max_selections=5)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)   
    
    ingredients_string=''
    
    for fruit_choosen  in  ingredients_list:
        ingredients_string+=fruit_choosen + ' '
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    time_to_inser = st.button("Submit Order")
    #st.write(my_insert_stmt)
    #st.stop()

    if time_to_inser:
        session.sql(my_insert_stmt).collect()
        st.success("""Your Smoothie is ordered , """ + name_on_order + """!""", icon="✅")
