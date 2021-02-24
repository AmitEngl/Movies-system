import requests
import streamlit as st
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import time

@st.cache
def get_recommendations(title, indices, sim_matrix,titles):
    '''
    :param title: movie title
    :param indices: indices list
    :param sim_matrix: similarity matrix
    :param titles: titles list of all movies
    :return: reccomandation list of 10 movies and their sim scores
    '''

    idx = indices.loc[title]
    if not isinstance(idx, (int, np.integer)):
        if len(idx) > 1:
            idx = idx[0]

    sim_scores = list(enumerate(sim_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    movie_indices = [i[0] for i in sim_scores]
    scores = [i[1] for i in sim_scores][:10]
    output = titles.iloc[movie_indices][:10]

    # output = np.unique(output)[:10]

    df = pd.DataFrame(output,columns=['title'])

    df['score'] = scores

    return df

@st.cache
def url_from_title(titles_list):
    '''
    :param titles_list: a list of movie titles
    :return: a list of the movies IMDB urls
    '''

    BASE_URL = 'https://www.imdb.com/title/'
    url_list = []
    for title in titles_list:
        imdb_id = md_df['imdb_id'][md_df['title'] == title].values[0]
        url_list.append(BASE_URL + imdb_id)

    return url_list

@st.cache
def get_img_src(url_list):
    '''
    gets a list of "IMDB" urls and scrapes for the movie poster image source
    :return: a list of urls of the images
    '''

    images_src = []

    # getting images source urls
    for i in url_list:

        try:
            page = requests.get(i)
            soup = BeautifulSoup(page.text, 'html.parser')
            poster_div = soup.find('div', {'class': 'poster'})
            images = poster_div.findAll('img')
        except:
            print('Error parsing the movie title page from url: {} '.format(i))
            images_src.append(None)
        else:
            # images_src.append(images[0]['src'].split('_V1_')[0]+ '_V1_') # for bigger images
            images_src.append(images[0]['src'])  # for small images

    return images_src

@st.cache
def load_files():
    '''
    loads the required files
    :return: md_df, indices, titles, sim_matrix
    '''
    md_df = pd.read_csv('movies_data.csv')
    indices = pd.Series(md_df.index, index=md_df['title'])
    titles = md_df['title']
    sim_matrix = np.load('cosine_sim.npz')
    sim_matrix = sim_matrix.f.arr_0

    return md_df, indices, titles, sim_matrix

# @st.cache
def merge_results(result_df_final, titles_list):
    '''
    merge results, clean duplications, gruops and sort final df
    :return: final df result after processing
    '''
    for title in titles_list:
        if title in result_df_final['title'].tolist():
            index = result_df_final[result_df_final['title'] == title].index
            # Delete these row indexes from dataFrame
            result_df_final.drop(index, inplace=True)

    result_df_final = result_df_final.groupby(['title']).sum()
    result_df_final.sort_values(['score'], ascending=False, inplace=True)

    return result_df_final

md_df, indices, titles, sim_matrix = load_files()

st.image('./itcflix.JPG', use_column_width=True)

# st.title('    Movie Recommendation System')
st.image('./movies background.jpeg', use_column_width=True)
st.header('Welcome to our movies recommendation system')
st.subheader('Choose your latest favorite movies')
# st.markdown('Streamlit is **_really_ cool**.')

# sidebar content
with st.sidebar.beta_expander("About"):
    st.text("This project is made by:\n"
                "Ohad Hayoun\nLoren Dery\nAmit Engelstein\nAlex Zabbal\nOr Granot\n\n")
    st.image('./main3.jpg', use_column_width=True)

with st.sidebar.beta_expander("Info"):
    st.write("Our Movie recommendation system\n"
                    "is based on an Hybrid model of\n"
                    "a Content Based Filtering model and \n"
                    "a Collaborative Filtering model")
    st.image('./main2.jpg', use_column_width=True)

st.sidebar.subheader('Your favorite movies:')

titles_list = []
start = 0

variables = st.multiselect("Enter movie title", md_df['title'])

left_column, mid, right_column = st.beta_columns(3)
with mid:
    enter = mid.button('Enter')
    if enter:
        titles_list = variables
        start = 1

if start == 1:
    url_list = url_from_title(titles_list)
    images_src = get_img_src(url_list)

    for i, movie in enumerate(titles_list):
        st.sidebar.write(str(i + 1) + ') ' + movie)
        st.sidebar.image(images_src[i], width=150)
        start = 2

if start == 2:
    st.write("Getting predictions...")

    # progress bar
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.03)
        my_bar.progress(percent_complete + 1)

    st.info('Success')
    title = titles_list[0]
    result_df_final = pd.DataFrame()

    # getting recommendations
    c1, c2 = st.beta_columns([3,1])
    with c1:
        for title in titles_list:
            result_df = get_recommendations(title, indices, sim_matrix,titles)
            result_df_final = pd.concat([result_df_final, result_df])

        result_df_final = merge_results(result_df_final,titles_list)
        result_df_final.reset_index(level=None, drop=False, inplace=True, col_level=0, col_fill='')

        for i,movie in enumerate(result_df_final['title'].iloc[:10]):
            st.write(str(i + 1) + ') ' + movie)
            time.sleep(0.4)

        with st.beta_expander("Check complete table with scores"):
            st.table(result_df_final)

    # getting top 10 results
    result = result_df_final['title'].iloc[:10]

    # getting images
    url_list = url_from_title(result)
    images_src = get_img_src(url_list)

    # presenting results
    with c2:
        for i,movie in enumerate(result):
            st.write(str(i+1) + ') ' + movie)
            st.image(images_src[i], width=200)
            # st.image(images_src[i], caption=str(i + 1) + ') ' + result[i], width=200)

    start = 0


# if __name__ == '__main__':
#     md_df, indices, titles, sim_matrix = load_files()
#     title = 'The Lord of the Rings: The Fellowship of the Ring'
#     result_df = get_recommendations(title, indices, sim_matrix, titles)
#
#     print(result_df)

#
#
# if __name__ == '__main__':
#     md_df, indices, titles, sim_matrix = load_files()
#     # title = 'The Dictator'
#     # title = 'Beauty and the Beast'
#     title = 'The Lord of the Rings: The Fellowship of the Ring'
#
#     titles_list = [title]
#     result_df_final = pd.DataFrame()
#     # 'The Beatles: Eight Days a Week - The Touring Years', 'Electric Dreams', 'RoboCop', 'Ted'
#
#     result_df = get_recommendations(title, indices, sim_matrix, titles)
#     # print(result_df)
#
#     result_df_final = pd.concat([result_df_final, result_df])
#
#     result_df_final = merge_results(result_df_final, titles_list)
#     result_df_final.reset_index(level=None, drop=False, inplace=True, col_level=0, col_fill='')
#
#
#     print(result_df_final)
