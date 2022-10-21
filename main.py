import streamlit as st
import json
import pickle
import numpy as np

with open('columns.json', 'r') as f:
  columns = json.load(f)['data_columns']
  locations = columns[3:]

global model

with open('banglore_home_prices_model.pickle', 'rb') as f:
  model = pickle.load(f)
  print("model loaded")

def get_estimated_price(location, sqft, bath, bhk):
  try:
    loc_index = locations.index(location.lower())
  except:
    loc_index = -1

  x = np.zeros(len(columns))
  print(f'x {x.shape}')
  x[0] = sqft
  x[1] = bath
  x[2] = bhk
  if loc_index >= 0:
      x[loc_index] = 1

  return round(model.predict([x])[0], 2)

st.title('Bengalore House Prices')

st.sidebar.header("Enter house specs")
sqft = st.sidebar.number_input("Area (sqft)", step=1)
bhk = st.sidebar.slider("BHK", 1, 5)
bath = st.sidebar.slider("Bath", 1, 5)
location = st.sidebar.selectbox("Location", locations)

if st.sidebar.button("Predict"):
  price = get_estimated_price(location, sqft, bhk, bath)
  st.write(f"Estimated price for property {price} lakh")