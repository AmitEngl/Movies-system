import requests
import streamlit as st
import pandas as pd
import difflib
import numpy as np
from bs4 import BeautifulSoup


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

def check_input(input,df):
    title = input.title()
    if title not in df['title'].values:
        return None
    else:
        return title

def get_recommendations(title, indices, sim_matrix,titles):
    idx = indices.loc[title]
    sim_scores = list(enumerate(sim_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]
    return titles.iloc[movie_indices][:10]

def url_from_title(titles_list):

    BASE_URL = 'https://www.imdb.com/title/'
    url_list = []
    for title in titles_list:
        imdb_id = md_df['imdb_id'][md_df['title'] == title].values[0]
        url_list.append(BASE_URL + imdb_id)

    return url_list

def get_img_src(url_list):

    images_src = []

    # getting images source urls
    for i in url_list:
        page = requests.get(i)
        soup = BeautifulSoup(page.text, 'html.parser')
        poster_div = soup.find('div', {'class': 'poster'})
        images = poster_div.findAll('img')
        # images_src.append(images[0]['src'].split('_V1_')[0]+ '_V1_') # for bigger images
        images_src.append(images[0]['src']) # for small images

    return images_src


md_df = pd.read_csv('movies_data.csv')
indices = pd.Series(md_df.index, index=md_df['title'])
titles = md_df['title']

# directory_path = get_image.check_folder()

st.image('./movies background.jpeg')
st.title('Movie Recommendation System')
st.header('Welcome to our Movies system recommendation system')
st.subheader('Choose your favorite latest movie')

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

if start == 1:
    title = titles_list[0]

    url_list = url_from_title(titles_list)
    images_src = get_img_src(url_list)

    for i in images_src:
        st.image(i)

    # loading files
    sim_matrix = np.load('cosine_sim.npz')
    sim_matrix = sim_matrix.f.arr_0

############################
    # mid.image('./posters/' + title + '.jpg')
    left_column, mid, right_column = st.beta_columns(3)
    pressed = mid.button('Run Model')
    if pressed:
        st.write("Getting predictions...")
        # st.write('Movies recommendations based on your watching history:')

        results = get_recommendations(title, indices, sim_matrix,titles).values

        # url_list = url_from_title(results)
        # images_src = get_img_src(url_list)

        results_flag = 1
        if results_flag == 1:
            st.info("Success")

            st.subheader('Your recommendations:')
            for i,movie in enumerate(results):
                st.write(str(i+1) + ') ' + movie)
            # for i,image in enumerate(images_src):
            #     st.image(image, caption= str(i+1) + ') ' + results[i], width=200)














            # for i,image in enumerate(images_src):
            #     # st.write(i+1,title)
            #     st.image(image, caption= str(i+1) + ') ' + results[i], width=200)

            # for i,title in enumerate(results):
            #     # st.write(i+1,title)
            #     st.image('./posters/' + title + '.jpg', caption= str(i+1) + ') ' + title, width=200)


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

#
# if __name__ == '__main__':
#
#     titles_list = ['Toy Story', 'Heat', 'Forrest Gump', '88 Minutes']
#     md_df = pd.read_csv('movies_data.csv')
#
#     src_list = get_img_src(md_df, titles_list)
#     print(src_list)