import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd

st.title('My first app')

st.write("HELLO WORLD!")

# Draw a title and some text to the app:
'''
# My first app
Here's our first attempt at using data to create a table:

This is some _markdown_.
'''

df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

df

x = 10
'x', x  # <-- Draw the string 'x' and then the value of x


# Line chart:
'''
# Demo line chart
'''
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)


# Map
'''
# Demo longitude/latitude data points against map:
'''
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)


# Widgets
'''
# Demo basic checkbox to show/hide data:
'''

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    st.line_chart(chart_data)

## Select box demo
#option = st.selectbox(
#    'Which number do you like best?',
#     df['first column'])
#
#'You selected: ', option

# select box in sidebar demo
option = st.sidebar.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected:', option

left_column, right_column = st.beta_columns(2)
pressed = left_column.button('Press me?')
if pressed:
    right_column.write("Woohoo!")

expander = st.beta_expander("FAQ")
expander.write("Here you could put in some really, really long explanations...")


# Qtrade use case:
'''
# Demo dividend dashboard

## Post authentication...

Users select:
* Account #
* Cadence
* Date range
* Expected dividends checkbox
* Actual dividends checkbox

Results update on a single line chart
'''

# First, let's make the dummy dataframes:
#foo = pd.DataFrame()
timeline = [
    "2019-03-03T00:00:00.000000-05:00",
    "2020-01-03T00:00:00.000000-05:00",
    "2020-02-11T00:00:00.000000-05:00",
    "2020-10-01T00:00:00.000000-05:00", # Date interpreted correctly
    "2020-06-26T00:00:00.000000-05:00",
]

foo = pd.DataFrame({
   'expected': [20, 18, 489, 675, 1776],
   'actual': [4, 25, 281, 600, 1900]
}, index=timeline)

foo

st.line_chart(foo)



'''
# Demo deposit monitor

## Post authentication...

Users select:
* Account #
* Cadence
* Date range

Results update on 2 line charts; top shows
deposits, bottom shows sum total against
market value.
'''