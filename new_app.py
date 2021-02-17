import streamlit as st
import pandas as pd
import get_image
import server_test01
import difflib

import os
import sys
import shutil
# from pyngrok import ngrok
# public_url = ngrok.connect('8501')
# public_url

def check_input(input,df):
    title = input.title()
    if title not in df['title'].values:
        return None
    else:
        return title

# directory_path = get_image.check_folder()

st.image('./movies background.jpeg')
st.title('Movie Recommendation System')
st.header('Welcome to our Movies system recommendation system')
st.subheader('This is a test - Choose your favorite latest movie')

def tests():
    # success
    st.success("Success")
    st.info("Information")
    st.warning("Warning")
    st.error("Error")

    # Selection box

    # first argument takes the titleof the selectionbox
    # second argument takes options
    hobby = st.selectbox("Hobbies: ",
                         ['Dancing', 'Reading', 'Sports'])

    # print the selected hobby
    st.write("Your hobby is: ", hobby)

    # multi select box

    # first argument takes the box title
    # second argument takes the options to show
    hobbies = st.multiselect("Hobbies: ",
                             ['Dancing', 'Reading', 'Sports'])

    # write the selected options
    st.write("You selected", len(hobbies), 'hobbies')

    # Create a simple button that does nothing
    st.button("Click me for no reason")

    # Create a button, that when clicked, shows a text
    if (st.button("About")):
        st.text("Welcome To GeeksForGeeks!!!")

    name = st.text_input("Enter Your name", "Type Here ...")

    # display the name when the submit button is clicked
    # .title() is used to get the input text string
    if (st.button('Submit')):
        result = name.title()
        st.success(result)


# csv_file = 'cleaned_movies.csv'
csv_file = 'movies_data.csv'
md_df = pd.read_csv(csv_file)
titles_list = []
start = 0
# getting user's input
user_input = st.text_input("Enter movie title")

# if st.checkbox('Enter'):
if user_input:
    user_input_check = check_input(user_input,md_df)
    # st.write('user_input_check',user_input_check)

    if not user_input_check:
        st.error('Movie title not found')
        st.write('Please retry or click below to check for similar movie titles')

        if st.checkbox('Find similar titles'):
            sim_titles = difflib.get_close_matches(user_input, md_df["title"].values)
            if sim_titles:
                for i in sim_titles:
                    st.write(i)

    else:
        user_input = user_input_check
        st.success(user_input)
        titles_list.append(user_input)
        start = 1

# titles_list = ['Toy Story 2', 'The Lion King','Jumanji']

# if st.checkbox('Start'):
if start == 1:
    title = titles_list[0]

    left_column, mid, right_column = st.beta_columns(3)

    get_image.main(md_df, titles_list)
    mid.image('./posters/' + title + '.jpg')

    pressed = mid.button('Run Model')
    if pressed:
        st.write("Getting predictions...")
        results = server_test01.get_prediction(title, md_df).values

        results = results[:2]

        # getting the recomendation images
        get_image.main(md_df, results)
        st.write('Movies recommendations based on your watching history:')
        for i,title in enumerate(results):
            # st.write(i+1,title)
            mid.image('./posters/' + title + '.jpg', caption= str(i+1) + ') ' + title, width=200)


# clear posters images folder
# get_image.clear_folder()


    # col1, col2, col3 = st.beta_columns(3)
    # with col1:
    #     st.header(titles_list[0])
    #     st.image('./posters/' +  titles_list[0] + '.jpg', use_column_width=True)
    #
    # with col2:
    #     st.header(titles_list[1])
    #     st.image('./posters/' +  titles_list[1] + '.jpg', use_column_width=True)
    #
    # with col3:
    #     st.header(titles_list[2])
    #     st.image('./posters/' +  titles_list[2] + '.jpg', use_column_width=True)
    #
    # option = st.selectbox('Which movie do like best?',titles_list)


# for i in titles_list:
#     image_name = i + '.jpg'
#     st.image('./posters/' + image_name, caption=i)

# Slider
# x = st.sidebar.slider('How do like drama movies?')
# st.write(x, 'Drama meter', x)

# left_column, right_column = st.beta_columns(2)
# pressed = left_column.button('Press me?')
# if pressed:
#     right_column.write("Woohoo!")

# st.write("Here's our first attempt at using data to create a table:")
# st.write(pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 20, 30, 40]
# }))
#
# # There are other data specific functions like st.dataframe() and st.table()
#
# # Slider
# x = st.sidebar.slider('Select a value')
# st.write(x, 'squared is', x * x)
#
# # Chart
# chart_data = pd.DataFrame(
#      np.random.randn(20, 3),
#      columns=['a', 'b', 'c'])
#
# st.line_chart(chart_data)
#
# map_data = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [32.08, 34.78],
#     columns=['lat', 'lon'])
#
# st.map(map_data)
#
#

#
# expander = st.beta_expander("FAQ")
# expander.write("Here you could put in some really, really long explanations...")


