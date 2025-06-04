import csv
import streamlit as st
import pandas as pd

# def color_positive_green(val):
#     """
#     Takes a scalar and returns a string with
#     the css property `'color: green'` for positive
#     strings, black otherwise.
#     """
#     if val > 0:
#         color = 'green'
#     else:
#         color = 'black'
#     return 'color: %s' % color

# def color_green():
#     return 'background-color: green'

# liste_des_gares = pd.read_csv('liste-des-gares.csv', sep=";")

# liste_des_gares.style.applymap(color_green, axis=1)

# st.dataframe(liste_des_gares)

def highlight_survived(s):
    return ['background-color: green']*len(s) if s.CODE_LIGNE else ['background-color: red']*len(s)

def color_survived(val):
    color = 'green' if val>500000 else 'red'
    return f'background-color: {color}'

df = pd.read_csv('liste-des-gares.csv', sep=";")
data_frame = df.style.map(color_survived, subset=['CODE_LIGNE'])
st.dataframe(data_frame)

# st.dataframe(df.style.apply(highlight_survived, axis=1))
# st.dataframe(df.style.map(color_survived, subset=['CODE_LIGNE']))
# st.dataframe(df.style.map(color_survived, subset=['CODE_LIGNE']))



