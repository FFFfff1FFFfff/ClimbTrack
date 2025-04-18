import streamlit as st

st.set_page_config(page_title="ClimbTrack MainPage", page_icon="🧗", layout="wide")

st.title("Welcome to ClimbTrack")
st.markdown("Climb higher, climb longer！")

st.image("https://images.unsplash.com/photo-1517836357463-d25dfeac3438", use_container_width =True)

st.markdown("## Page Guide")
st.page_link("pages/profile.py", label="Check Personal Profile", icon="🧍‍♂️")

