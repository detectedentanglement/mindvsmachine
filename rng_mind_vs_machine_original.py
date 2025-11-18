import streamlit as st
import random

st.set_page_config(page_title="Mind vs Machine RNG", layout="centered")

st.title("🧠 Mind vs Machine 🎲")
st.subheader("Try to influence the random number...")

min_val = 0
max_val = 99

if 'last_number' not in st.session_state:
    st.session_state.last_number = None

col1, col2 = st.columns(2)

with col1:
    if st.button("🎲 Generate Number"):
        st.session_state.last_number = random.randint(min_val, max_val)

with col2:
    if st.button("🔄 Reset"):
        st.session_state.last_number = None

if st.session_state.last_number is not None:
    st.markdown(f"## 🎯 Number: **{st.session_state.last_number}**")

st.markdown("---")
st.markdown("Close your eyes. Focus on a number. Then hit **Generate**. Log your intent. Look for patterns.")
