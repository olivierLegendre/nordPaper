import csv
import streamlit as st
import pandas as pd

def color_positive_green(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: green'` for positive
    strings, black otherwise.
    """
    if val > 0:
        color = 'green'
    else:
        color = 'black'
    return 'color: %s' % color

liste_des_gares = pd.read_csv('liste-des-gares.csv', sep=";")

liste_des_gares.style.applymap(color_positive_green)

st.dataframe(liste_des_gares)




