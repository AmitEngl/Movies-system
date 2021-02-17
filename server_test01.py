import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask
from flask import request
import os
import difflib
import warnings

warnings.simplefilter('ignore')

app = Flask(__name__)

features = ['Movie1']
movies_df = pd.read_csv('movies_data.csv')

def get_features_table():
    html = '''
            <table style="width:100%">
            <tr>
            '''
    for feature in features:
        html += '<th><label for="'
        html += feature
        html += '">'
        if feature == 'Statues':
            html += 'Status (1 - Developed; 0 - Developing)'
        else:
            html += feature
        html += '</label></th>'
    html += '</tr><tr>'

    for feature in features:
        html += '<th><input type="text" id="'
        html += feature
        html += '" name="'
        html += feature
        html += '" ></th>'
    html += '</tr></table><br>'

    return html

def get_prediction(movie_name, movies_df):

    # movie_name = movie_name['Movie1'][0].strip()

    # movies_df = pd.read_csv('movies_data.csv')
    titles = movies_df['title']

    count = CountVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
    count_matrix = count.fit_transform(movies_df['soup'])

    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    movies_df = movies_df.reset_index()
    indices = pd.Series(movies_df.index, index=movies_df['title'])

    def get_recommendations(title):
        idx = indices[title]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:31]
        movie_indices = [i[0] for i in sim_scores]
        return titles.iloc[movie_indices]

    # movie_name = 'The Dark Knight'

    result = get_recommendations(movie_name).head(10)

    print(result.to_dict().values)
    # print(result.to_dict())

    return result

@app.route('/')
def index():
    html = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Movies system recommendation program</title>
            </head>
            <body>
            <h2>
                Welcome to our Movies system recommendation system<br>
                Choose your favorite latest movie:
            </h2>

            <form action="/predict_movie">
            '''
    html += get_features_table()
    html += '''
        <input type="submit" value="Submit">
        </form>

        <p>Click the "Submit" button when finished.</p>

        </body>
        </html>
        '''
    return html


@app.route("/predict_movie", methods=["GET"])
def predict_movie():

    dict_for_prediction = request.args.to_dict(flat=False)
    if len(dict_for_prediction) == len(features) and not [''] in list(dict_for_prediction.values()):
        html = '''
                <!DOCTYPE html>
                    <html>
                    <head>
                    <style>
                    table {
                      font-family: arial, sans-serif;
                      border-collapse: collapse;
                      width: 100%;
                    }
                    td, th {
                      border: 1px solid #dddddd;
                      text-align: left;
                      padding: 8px;
                    }
                    tr:nth-child(even) {
                      background-color: #dddddd;
                    }
                    </style>
                    </head>
                    <body>
                    <h2>Movies recommendations</h2>
                    <table>
                      <tr>
                '''
        for feature in features:
            html += '<th>'
            html += feature
            html += '</th>'
        html += '<th>Recommendations</th>'
        html += '</tr><tr>'
        for item in dict_for_prediction.items():
            title = str(item[1][0]).strip().title()

            if title not in movies_df['title'].values:
                return f'Movie title not found - Please retry  --->  Similar titles found: {difflib.get_close_matches(title, movies_df["title"].values)}'

            html += '<td>'
            html += title
            html += '</td>'
        results = get_prediction(title,movies_df).values

        # results = ['df','dfs','34','ii9','36666']   #################

        html += '<td>'
        html += results[0] + ', / ' + results[1] + ', / ' + results[2] + ', / ' + results[3]+ ', / ' + results[4]
        html += '</td>'
        html += '''
                </tr></table>
                </body>
                </html>
                '''
        return html

    return 'Invalid Input'

def main():
    app.run()


if __name__ == '__main__':
    port = os.environ.get('PORT')

    if port:
        app.run(host='0.0.0.0', port=int(port),debug=True)
    else:
        app.run()