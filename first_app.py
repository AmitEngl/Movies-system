import streamlit as st
import numpy as np
import pandas as pd


st.title('My first app')

st.header('My header')
st.subheader('I am testing this app')

st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))

# There are other data specific functions like st.dataframe() and st.table()

# Slider
x = st.sidebar.slider('Select a value')
st.write(x, 'squared is', x * x)

# Chart
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [32.08, 34.78],
    columns=['lat', 'lon'])

st.map(map_data)


if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

st.line_chart(chart_data)

option = st.sidebar.selectbox(
    'Which number do you like best?',
    ['a', 'b', 'c'])

'You selected: ', option

left_column, right_column = st.beta_columns(2)
pressed = left_column.button('Press me?')
if pressed:
    right_column.write("Woohoo!")

expander = st.beta_expander("FAQ")
expander.write("Here you could put in some really, really long explanations...")


st.image('./dog2.jpg')