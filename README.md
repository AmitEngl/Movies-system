# Movies Recommendation System
2nd project of the ITC data science program 

#### Created by:
* Ohad Hayoun 
* Amit Englstein
* Or Granot 
* Alex Zabbal 
* Loren Dery

## Description
This is a recommendation system for movies based on the Movie Lens dataset.

<https://www.kaggle.com/rounakbanik/the-movies-dataset>

The main steps of the project using the dataset:
* Data Cleaning and Feature Selection
* EDA	
* Modeling
  - Content-Based Filtering	
  - Collaborative Filtering	
  - Hybrid Model
* Deployment	

## Requirements
* nnfs~=0.5.1
* python-dateutil~=2.8.1
* requests~=2.25.1
* scikit-learn~=0.24.0
* urllib3~=1.26.2
* pandas~=1.1.3
* streamlit~=0.76.0
* bs4~=0.0.1

## Required files (master branch)
* movies_eda.ipynb
* Baseline.ipynb
* content_based_filtering.ipynb
* Hybrid.ipynb

## Required files (Ohad2 branch) -> deployment 
* cosine_sim.npz
* movies background.jpeg
* new_app.py
* requirements.txt
* setup.sh
* itcflix.JPG
* main1.JPG
* movies_data.csv
* Procfile


## How to use
1. Clone the deployment brach (Ohad2) into a folder 
2. From the terminal, run: streamlit run new_app.py
3. Insert your latest favorite movies and press enter 

