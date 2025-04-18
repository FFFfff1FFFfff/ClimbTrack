import streamlit as st

st.set_page_config(page_title="My Profile", page_icon="🧍", layout="centered")

st.title("My Climbing Record")

name = st.text_input("Name", "Oi")
level_B = st.selectbox("Current Bouldering Level", ["V0-V1", "V2-V3", "V4-V5", "V6+"])
level_T = st.selectbox("Current Top Roping Level", ["5.9-", "5.10", "5.11", "5.12+"])
fav_route = st.text_input("Favourite Style", "Balance")

if st.button("Saved"):
    st.success(f"Saved：{name}（{level_B}）（{level_T}）{fav_route}")
